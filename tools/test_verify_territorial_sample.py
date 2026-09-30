"""Offline checks for the bounded INE ↔ GEO API PT sample verifier."""
from __future__ import annotations

import unittest

from verify_territorial_sample import municipality_categories, summarize_municipality


def geo_response(dtmn: object = "0113") -> dict:
    return {
        "url": "https://json.geoapi.pt/municipio/Oliveira%20de%20Azem%C3%A9is",
        "status": 200,
        "bytes": 123,
        "sha256": "fixture",
        "fetched_at_utc": "2026-09-30T19:00:00+00:00",
        "json": {
            "nome": "Oliveira de Azeméis",
            "dtmn": dtmn,
            "codigoine": dtmn,
            "geojson": {
                "type": "Feature",
                "properties": {"Dicofre": dtmn},
                "geometry": {"type": "Polygon", "coordinates": []},
                "bbox": [-9, 40, -8, 41],
            },
        },
    }


class TerritorialSampleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.categories = {
            "0008273": [{"name": "Oliveira de Azeméis", "code": "11A0113"}],
            "0012918": [{"name": "Oliveira de Azeméis", "code": "1A0113"}],
        }

    def test_categories_only_take_municipality_level(self) -> None:
        metadata = {"Dimensoes": {"Categoria_Dim": [
            {"Dim2": [
                {"dim_num": "2", "categ_nivel": "4", "categ_cod": "11A", "categ_dsg": "Região"},
                {"dim_num": "2", "categ_nivel": "5", "categ_cod": "11A0113", "categ_dsg": "Oliveira de Azeméis"},
            ]}
        ]}}
        self.assertEqual(municipality_categories(metadata), self.categories["0008273"])

    def test_leading_zero_is_kept_but_pair_is_not_approved(self) -> None:
        result = summarize_municipality(geo_response(), self.categories)
        self.assertEqual(result["dtmn"], "0113")
        self.assertEqual(result["status"], "candidate_needs_manual_evidence")
        self.assertEqual(result["ine_candidates_by_indicator"]["0008273"][0]["code"], "11A0113")
        self.assertFalse(result["approved_correspondence"])
        self.assertFalse(result["geometry_equivalence_confirmed"])

    def test_numeric_code_and_missing_metadata_are_unresolved(self) -> None:
        numeric = summarize_municipality(geo_response(113), self.categories)
        self.assertIn("municipal_code_not_string", numeric["problems"])
        self.assertEqual(numeric["status"], "unresolved")
        incomplete = summarize_municipality(geo_response(), {"0008273": self.categories["0008273"]})
        self.assertIn("ine_metadata_unavailable", incomplete["problems"])
        self.assertEqual(incomplete["status"], "unresolved")


if __name__ == "__main__":
    unittest.main()
