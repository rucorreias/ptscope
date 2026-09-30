"""Offline checks for the INE population verifier's geography accounting."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from verify_ine_population_scope import summarize_observations, write_summary


class PopulationScopeSummaryTests(unittest.TestCase):
    def test_unknown_geography_is_not_silently_counted_as_known(self) -> None:
        response = {
            "url": "https://example.invalid/filtered",
            "endpoint": "https://example.invalid/filtered",
            "params": {"Dim1": "S7A2023"},
            "status": 200,
            "bytes": 1,
            "sha256": "abc",
            "json": [{
                "Dados": {"2023": [
                    {"geocod": "PT", "valor": "100"},
                    {"geocod": "1312", "valor": "10"},
                    {"geocod": "9999", "valor": "1"},
                ]},
            }],
        }
        result = summarize_observations(response, {"1312", "0113"}, {"PT"})
        self.assertEqual(result["observed_municipality_count"], 1)
        self.assertEqual(result["missing_municipality_count"], 1)
        self.assertEqual(result["missing_municipality_examples"], ["0113"])
        self.assertEqual(result["unrecognised_geography_count"], 1)
        self.assertEqual(result["unrecognised_geography_examples"], ["9999"])

    def test_summary_keeps_audit_fields_per_period(self) -> None:
        run = {
            "queried_at_utc": "2026-09-30T19:00:00+00:00",
            "scope": "filtered",
            "indicators": {
                "0008273": {
                    "metadata": {
                        "request": {"sha256": "meta-hash"},
                        "periods": [{"code": "S7A2023", "label": "2023"}],
                    },
                    "observations_by_period": {
                        "2023": {
                            "request": {
                                "url": "https://example.invalid/filtered",
                                "status": 200,
                                "sha256": "data-hash",
                            },
                            "row_count": 3,
                            "expected_municipality_count": 2,
                            "observed_municipality_count": 1,
                            "missing_municipality_count": 1,
                            "unrecognised_geography_count": 1,
                            "rows_without_valor_count": 0,
                            "qualifier_fields": [],
                            "data_extraction": "2026-09-30",
                        },
                    },
                },
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "summary.json"
            write_summary(path, run)
            summary = json.loads(path.read_text(encoding="utf-8"))
        period = summary["indicators"]["0008273"]["periods"][0]
        self.assertEqual(period["period_code"], "S7A2023")
        self.assertEqual(period["sha256"], "data-hash")
        self.assertEqual(period["unrecognised_geography_count"], 1)


if __name__ == "__main__":
    unittest.main()
