#!/usr/bin/env python3
"""Small manual INE ↔ GEO API PT municipality comparison; never approves joins."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

INE_BASE = "https://www.ine.pt/ine/json_indicador/pindicaMeta.jsp"
GEO_BASE = "https://json.geoapi.pt/municipio"
INDICATORS = {"0008273": "NUTS 2013 / 03505", "0012918": "NUTS 2024 / 05257"}
SAMPLES = {
    "porto": "Porto",
    "lisboa": "Lisboa",
    "Oliveira de Azeméis": "Oliveira de Azeméis",
    "corvo": "Corvo",
    "funchal": "Funchal",
}


def fetch(url: str, timeout: float) -> dict[str, Any]:
    command = [
        "curl", "-sS", "-L", "-H", "Accept: application/json",
        "-H", "User-Agent: PTScope/0.1 manual territorial validation",
        "-w", "\n%{http_code}", url,
    ]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
        if completed.returncode:
            raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))
        body, status_raw = completed.stdout.rsplit(b"\n", 1)
        status = int(status_raw)
        if status != 200:
            raise RuntimeError(f"HTTP {status}: {body[:200]!r}")
        return {
            "url": url,
            "status": status,
            "bytes": len(body),
            "sha256": hashlib.sha256(body).hexdigest(),
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
            "json": json.loads(body),
        }
    except (ValueError, json.JSONDecodeError, RuntimeError, subprocess.TimeoutExpired) as exc:
        return {"url": url, "fetched_at_utc": datetime.now(timezone.utc).isoformat(), "error": repr(exc)}


def municipality_categories(metadata: dict[str, Any]) -> list[dict[str, str]]:
    categories = []
    for group in metadata["Dimensoes"]["Categoria_Dim"]:
        for values in group.values():
            categories.extend(
                {"code": item["categ_cod"], "name": item["categ_dsg"]}
                for item in values
                if item["dim_num"] == "2" and item.get("categ_nivel") == "5"
            )
    return categories


def candidates_for_name(name: str, categories: list[dict[str, str]]) -> list[dict[str, str]]:
    # Names are used only to locate candidates, never as proof of correspondence.
    return [item for item in categories if item["name"].strip().casefold() == name.strip().casefold()]


def summarize_municipality(
    response: dict[str, Any], categories: dict[str, list[dict[str, str]]]
) -> dict[str, Any]:
    if "error" in response:
        return {"request": response, "status": "unresolved", "reason": "request_failed"}
    data = response["json"]
    if not isinstance(data, dict):
        return {"request": {k: response[k] for k in ("url", "status", "bytes", "sha256", "fetched_at_utc")},
                "status": "unresolved", "reason": "unexpected_payload"}
    feature = data.get("geojson") or {}
    properties = feature.get("properties") or {}
    name = data.get("nome")
    dtmn = data.get("dtmn")
    codigoine = data.get("codigoine")
    ine_candidates = {
        indicator: candidates_for_name(name, items) if isinstance(name, str) else []
        for indicator, items in categories.items()
    }
    problems = []
    if not isinstance(dtmn, str) or not isinstance(codigoine, str):
        problems.append("municipal_code_not_string")
    elif dtmn != codigoine:
        problems.append("dtmn_codigoine_disagree")
    if not isinstance(properties.get("Dicofre"), str):
        problems.append("feature_code_not_string")
    elif properties["Dicofre"] != dtmn:
        problems.append("feature_code_disagrees")
    if set(ine_candidates) != set(INDICATORS):
        problems.append("ine_metadata_unavailable")
    if not isinstance(name, str) or any(len(found) != 1 for found in ine_candidates.values()):
        problems.append("ine_category_missing_or_ambiguous")
    if not feature.get("geometry"):
        problems.append("geometry_missing")
    return {
        "request": {k: response[k] for k in ("url", "status", "bytes", "sha256")},
        "provider": "GEO API PT",
        "declared_cartographic_source": "DGT / CAOP 2024.1 (provider website)",
        "name": name,
        "dtmn": dtmn,
        "codigoine": codigoine,
        "feature_dicofre": properties.get("Dicofre"),
        "geometry_type": (feature.get("geometry") or {}).get("type"),
        "bbox": feature.get("bbox"),
        "ine_candidates_by_indicator": ine_candidates,
        "status": "unresolved" if problems else "candidate_needs_manual_evidence",
        "problems": problems,
        "approved_correspondence": False,
        "geometry_equivalence_confirmed": False,
        "crs_confirmed": False,
        "reuse_conditions_confirmed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/ptscope_territorial_sample.json")
    parser.add_argument("--timeout", type=float, default=25.0)
    parser.add_argument("--delay", type=float, default=0.75)
    args = parser.parse_args()
    if args.timeout <= 0 or args.delay < 0:
        parser.error("timeout must be positive and delay non-negative")

    result: dict[str, Any] = {
        "queried_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Two INE metadata requests and five selected GEO API PT municipalities",
        "metadata": {},
        "municipalities": {},
        "rule": "Names locate candidates only; no pair is automatically approved.",
    }
    categories: dict[str, list[dict[str, str]]] = {}
    for indicator, classification in INDICATORS.items():
        url = INE_BASE + "?" + urllib.parse.urlencode({"varcd": indicator, "lang": "PT"})
        response = fetch(url, args.timeout)
        if "error" in response:
            result["metadata"][indicator] = {"url": url, "error": response["error"]}
        else:
            try:
                categories[indicator] = municipality_categories(response["json"][0])
                result["metadata"][indicator] = {
                    "url": url, "status": response["status"], "sha256": response["sha256"],
                    "bytes": response["bytes"], "fetched_at_utc": response["fetched_at_utc"],
                    "classification": classification,
                    "municipality_count": len(categories[indicator]),
                }
            except (KeyError, IndexError, TypeError, ValueError) as exc:
                result["metadata"][indicator] = {"url": url, "error": repr(exc)}
        time.sleep(args.delay)

    for slug, label in SAMPLES.items():
        url = GEO_BASE + "/" + urllib.parse.quote(slug, safe="")
        response = fetch(url, args.timeout)
        result["municipalities"][label] = summarize_municipality(response, categories)
        Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        time.sleep(args.delay)

    print(args.output)


if __name__ == "__main__":
    main()
