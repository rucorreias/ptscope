#!/usr/bin/env python3
"""Small manual verifier for INE municipal population indicators.

This script intentionally performs a narrow set of filtered requests. It is
not part of the normal test suite and should not be run by CI.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
import urllib.parse
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = "https://www.ine.pt/ine/json_indicador"
INDICATORS = ("0008273", "0012918")


def build_url(endpoint: str, params: dict[str, str]) -> str:
    return f"{BASE}/{endpoint}?{urllib.parse.urlencode(params)}"


def fetch_json(endpoint: str, params: dict[str, str], timeout: float) -> dict[str, Any]:
    url = build_url(endpoint, params)
    command = [
        "curl",
        "-sS",
        "-L",
        "-G",
        f"{BASE}/{endpoint}",
        "-H",
        "Accept: application/json",
        "-H",
        "User-Agent: PTScope/0.1 manual INE validation",
    ]
    for key, value in params.items():
        command.extend(["--data-urlencode", f"{key}={value}"])
    command.extend(["-w", "\n%{http_code}"])

    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.decode("utf-8", errors="replace"))

    output = completed.stdout.rsplit(b"\n", 1)
    if len(output) != 2:
        raise RuntimeError("curl output did not include an HTTP status code")
    body, status_raw = output
    status = int(status_raw.decode("ascii"))
    if status >= 400:
        raise RuntimeError(f"HTTP {status}: {body[:200]!r}")

    return {
        "url": url,
        "endpoint": f"{BASE}/{endpoint}",
        "params": params,
        "status": status,
        "bytes": len(body),
        "sha256": hashlib.sha256(body).hexdigest(),
        "json": json.loads(body),
    }


def fetch_json_with_retries(
    endpoint: str,
    params: dict[str, str],
    timeout: float,
    retries: int,
    delay: float,
) -> dict[str, Any]:
    last_error: str | None = None
    for attempt in range(retries + 1):
        try:
            return fetch_json(endpoint, params, timeout)
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            last_error = repr(exc)
            if attempt < retries:
                time.sleep(delay * (attempt + 1))

    return {
        "url": build_url(endpoint, params),
        "endpoint": f"{BASE}/{endpoint}",
        "params": params,
        "error": last_error,
    }


def flatten_categories(meta: dict[str, Any]) -> list[dict[str, str]]:
    categories: list[dict[str, str]] = []
    for group in meta["Dimensoes"]["Categoria_Dim"]:
        for values in group.values():
            categories.extend(values)
    return categories


def period_codes(meta: dict[str, Any]) -> list[tuple[str, str]]:
    categories = flatten_categories(meta)
    periods = [
        (category["categ_cod"], category["categ_dsg"])
        for category in categories
        if category["dim_num"] == "1"
    ]
    return sorted(periods, key=lambda item: item[1])


def municipality_codes(meta: dict[str, Any]) -> set[str]:
    return {
        category["categ_cod"]
        for category in flatten_categories(meta)
        if category["dim_num"] == "2" and category.get("categ_nivel") == "5"
    }


def nonmunicipality_codes(meta: dict[str, Any]) -> set[str]:
    return {
        category["categ_cod"]
        for category in flatten_categories(meta)
        if category["dim_num"] == "2" and category.get("categ_nivel") != "5"
    }


def summarize_metadata(response: dict[str, Any]) -> dict[str, Any]:
    if "error" in response:
        return {"request": response, "error": response["error"]}

    meta = response["json"][0]
    categories = flatten_categories(meta)
    geography_levels = Counter(
        category["categ_nivel"]
        for category in categories
        if category["dim_num"] == "2"
    )
    dimensions = meta["Dimensoes"]["Descricao_Dim"]
    return {
        "request": {
            key: response[key]
            for key in ("url", "endpoint", "params", "status", "bytes", "sha256")
        },
        "indicator": {
            key: meta.get(key)
            for key in (
                "IndicadorCod",
                "IndicadorNome",
                "Periodic",
                "PrimeiroPeriodo",
                "UltimoPeriodo",
                "UnidadeMedida",
                "Potencia10",
                "PrecisaoDecimal",
                "DataUltimaAtualizacao",
                "DataExtracao",
            )
        },
        "dimensions": dimensions,
        "category_counts_by_dimension": dict(
            sorted(Counter(category["dim_num"] for category in categories).items())
        ),
        "geography_counts_by_level": dict(sorted(geography_levels.items())),
        "periods": [
            {"code": code, "label": label}
            for code, label in period_codes(meta)
        ],
    }


def data_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for by_period in payload["Dados"].values():
        rows.extend(by_period)
    return rows


def summarize_observations(
    response: dict[str, Any],
    expected_municipality_codes: set[str],
    known_nonmunicipality_codes: set[str],
) -> dict[str, Any]:
    if "error" in response:
        return {"request": response, "error": response["error"]}

    payload = response["json"][0]
    rows = data_rows(payload)
    observed_geography_codes = {
        str(row["geocod"]) for row in rows if row.get("geocod") is not None
    }
    observed_municipality_codes = observed_geography_codes & expected_municipality_codes
    # The response has no municipality-level field. Codes outside the metadata
    # cannot safely be classified as municipalities.
    unrecognised_geography_codes = (
        observed_geography_codes
        - expected_municipality_codes
        - known_nonmunicipality_codes
    )
    qualifier_fields = sorted(
        {
            key
            for row in rows
            for key in row
            if key.startswith("sinal") or "qual" in key.lower()
        }
    )
    missing_value_rows = [
        {
            "geocod": row.get("geocod"),
            "geodsg": row.get("geodsg"),
            "fields": sorted(row),
        }
        for row in rows
        if "valor" not in row
    ][:10]
    return {
        "request": {
            key: response[key]
            for key in ("url", "endpoint", "params", "status", "bytes", "sha256")
        },
        "data_extraction": payload.get("DataExtracao"),
        "last_update": payload.get("DataUltimoAtualizacao"),
        "last_period": payload.get("UltimoPref"),
        "row_count": len(rows),
        "expected_municipality_count": len(expected_municipality_codes),
        "observed_municipality_count": len(observed_municipality_codes),
        "missing_municipality_count": len(
            expected_municipality_codes - observed_municipality_codes
        ),
        "unrecognised_geography_count": len(unrecognised_geography_codes),
        "unrecognised_geography_examples": sorted(unrecognised_geography_codes)[:10],
        "missing_municipality_examples": sorted(
            expected_municipality_codes - observed_municipality_codes
        )[:10],
        "rows_without_valor_count": sum(1 for row in rows if "valor" not in row),
        "qualifier_fields": qualifier_fields,
        "missing_value_examples": missing_value_rows,
        "sample_rows": rows[:3],
    }


def write_run(output: Path, run: dict[str, Any]) -> None:
    output.write_text(json.dumps(run, ensure_ascii=False, indent=2), encoding="utf-8")


def write_summary(output: Path, run: dict[str, Any]) -> None:
    """Write a small per-period audit record; the full run remains separate."""
    summary: dict[str, Any] = {
        "queried_at_utc": run["queried_at_utc"],
        "scope": run["scope"],
        "indicators": {},
    }
    for indicator, result in run["indicators"].items():
        metadata = result["metadata"]
        periods = {
            period["label"]: period["code"] for period in metadata.get("periods", [])
        }
        entries = []
        for label, observation in result["observations_by_period"].items():
            request = observation.get("request", {})
            entries.append({
                "period": label,
                "period_code": periods.get(label),
                "url": request.get("url"),
                "status": request.get("status"),
                "sha256": request.get("sha256"),
                "row_count": observation.get("row_count"),
                "expected_municipality_count": observation.get("expected_municipality_count"),
                "observed_municipality_count": observation.get("observed_municipality_count"),
                "missing_municipality_count": observation.get("missing_municipality_count"),
                "unrecognised_geography_count": observation.get("unrecognised_geography_count"),
                "rows_without_valor_count": observation.get("rows_without_valor_count"),
                "qualifier_fields": observation.get("qualifier_fields"),
                "data_extraction": observation.get("data_extraction"),
                "last_update": observation.get("last_update"),
                "error": observation.get("error"),
            })
        summary["indicators"][indicator] = {
            "metadata_sha256": metadata.get("request", {}).get("sha256"),
            "metadata_error": metadata.get("error"),
            "periods": entries,
        }
    output.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/ptscope_ine_population_scope.json")
    parser.add_argument(
        "--summary-output", default="/tmp/ptscope_ine_population_scope_summary.json"
    )
    parser.add_argument("--delay", type=float, default=0.5)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=1)
    args = parser.parse_args()

    output = Path(args.output)
    summary_output = Path(args.summary_output)
    run: dict[str, Any] = {
        "queried_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": (
            "INE metadata for 0008273 and 0012918; annual observations filtered "
            "to Sexo=HM and Grupo etario=Total, with geography left open."
        ),
        "indicators": {},
    }

    for indicator in INDICATORS:
        meta_response = fetch_json_with_retries(
            "pindicaMeta.jsp",
            {"varcd": indicator, "lang": "PT"},
            args.timeout,
            args.retries,
            args.delay,
        )
        if "error" in meta_response:
            run["indicators"][indicator] = {
                "metadata": summarize_metadata(meta_response),
                "observations_by_period": {},
            }
            write_run(output, run)
            write_summary(summary_output, run)
            continue

        meta = meta_response["json"][0]
        indicator_result: dict[str, Any] = {
            "metadata": summarize_metadata(meta_response),
            "observations_by_period": {},
        }
        run["indicators"][indicator] = indicator_result
        write_run(output, run)
        write_summary(summary_output, run)
        time.sleep(args.delay)

        for period_code, period_label in period_codes(meta):
            data_response = fetch_json_with_retries(
                "pindica.jsp",
                {
                    "op": "2",
                    "varcd": indicator,
                    "Dim1": period_code,
                    "Dim3": "T",
                    "Dim4": "T",
                    "lang": "PT",
                },
                args.timeout,
                args.retries,
                args.delay,
            )
            indicator_result["observations_by_period"][period_label] = (
                summarize_observations(
                    data_response,
                    municipality_codes(meta),
                    nonmunicipality_codes(meta),
                )
            )
            write_run(output, run)
            write_summary(summary_output, run)
            time.sleep(args.delay)

    print(output)
    print(summary_output)


if __name__ == "__main__":
    main()
