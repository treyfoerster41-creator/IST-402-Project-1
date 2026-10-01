"""Saved hotel checks use an isolated SQLite file and synthetic place data."""

import os
import sqlite3
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.database import initialize_database
from backend.app.main import app


def save_request(place_id="synthetic-place-1", zip_code="16802"):
    return {
        "zip_code": zip_code,
        "center": {
            "postcode": zip_code,
            "country_code": "us",
            "latitude": 40.8 if zip_code == "16802" else 42.35,
            "longitude": -77.9 if zip_code == "16802" else -71.06,
            "locality": "Synthetic Town",
        },
        "hotel": {
            "place_id": place_id,
            "name": "Synthetic Hotel",
            "address": "1 Example Street",
            "latitude": 40.81,
            "longitude": -77.91,
        },
    }


class SavedHotelTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.db_path = Path(self.temp_dir.name) / "activity-test.db"
        self.env_patch = patch.dict(os.environ, {"EXPEDIA_LITE_DB_PATH": str(self.db_path)})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        initialize_database()
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.db_path)
        db.execute("PRAGMA foreign_keys = ON")
        try:
            yield db
            db.commit()
        finally:
            db.close()

    def test_additive_schema_has_defaults_keys_and_keeps_supplied_records(self):
        with self.connect() as db:
            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
            self.assertTrue({"saved_hotels", "saved_hotel_zips", "demo_hotel_nights"} <= tables)
            self.assertEqual(db.execute("SELECT count(*) FROM hotels").fetchone()[0], 8)
            self.assertEqual(db.execute("SELECT count(*) FROM trips").fetchone()[0], 12)
            self.assertEqual(db.execute("SELECT count(*) FROM users").fetchone()[0], 6)
            self.assertEqual(db.execute("SELECT count(*) FROM bookings").fetchone()[0], 6)
            columns = {row[1]: row for row in db.execute("PRAGMA table_info(demo_hotel_nights)")}
            self.assertEqual(columns["hotel_id"][5], 1)
            self.assertEqual(columns["stay_date"][5], 2)
            self.assertEqual(columns["nightly_rate_cents"][4], "10000")
            self.assertEqual(columns["rooms_available"][4], "20")
            foreign_keys = db.execute("PRAGMA foreign_key_list(demo_hotel_nights)").fetchall()
            self.assertTrue(any(row[2] == "saved_hotels" and row[3] == "hotel_id" for row in foreign_keys))
        initialize_database()
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM bookings").fetchone()[0], 6)

    def test_save_and_local_lookup_seed_only_five_demo_nights(self):
        response = self.client.post("/api/hotels/saved", json=save_request())
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()["created"])
        nights = response.json()["hotel"]["demo_nights"]
        self.assertEqual([night["stay_date"] for night in nights], [
            "2026-10-10", "2026-10-11", "2026-10-12", "2026-10-13", "2026-10-14",
        ])
        self.assertTrue(all(night["nightly_rate_cents"] == 10000 and night["rooms_available"] == 20 for night in nights))
        with patch("backend.app.main.search_nearby_hotels") as api_search:
            saved = self.client.get("/api/hotels/saved", params={"zip_code": "16802"})
        api_search.assert_not_called()
        self.assertEqual(saved.status_code, 200)
        self.assertEqual(saved.json()["center"]["postcode"], "16802")
        self.assertEqual(saved.json()["saved_ids"], ["synthetic-place-1"])
        self.assertEqual(len(saved.json()["hotels"]), 1)
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotel_zips").fetchone()[0], 1)

    def test_repeat_save_preserves_edited_night_and_new_zip_association(self):
        self.client.post("/api/hotels/saved", json=save_request())
        with self.connect() as db:
            db.execute(
                """UPDATE demo_hotel_nights SET nightly_rate_cents = 500, rooms_available = 10
                   WHERE hotel_id = ? AND stay_date = ?""",
                ("synthetic-place-1", "2026-10-10"),
            )
        repeated = self.client.post("/api/hotels/saved", json=save_request())
        self.assertEqual(repeated.status_code, 201)
        self.assertFalse(repeated.json()["created"])
        self.assertEqual(repeated.json()["hotel"]["demo_nights"][0]["nightly_rate_cents"], 500)
        self.assertEqual(repeated.json()["hotel"]["demo_nights"][0]["rooms_available"], 10)
        second_zip = self.client.post("/api/hotels/saved", json=save_request(zip_code="02108"))
        self.assertFalse(second_zip.json()["created"])
        self.assertEqual(self.client.get("/api/hotels/saved", params={"zip_code": "02108"}).json()["hotels"][0]["place_id"], "synthetic-place-1")
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotels").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotel_zips").fetchone()[0], 2)
            self.assertEqual(db.execute("SELECT count(*) FROM demo_hotel_nights").fetchone()[0], 5)

    def test_remove_cascades_only_its_local_records(self):
        self.client.post("/api/hotels/saved", json=save_request())
        self.client.post("/api/hotels/saved", json=save_request(place_id="synthetic-place-2"))
        removed = self.client.delete("/api/hotels/saved/synthetic-place-1")
        self.assertEqual(removed.status_code, 200)
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotels").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotel_zips").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT count(*) FROM demo_hotel_nights").fetchone()[0], 5)
            self.assertEqual(db.execute("SELECT count(*) FROM hotels").fetchone()[0], 8)
        self.assertEqual(self.client.delete("/api/hotels/saved/synthetic-place-1").status_code, 404)

    def test_invalid_zip_or_location_is_rejected_without_writes(self):
        invalid = save_request(zip_code="02108")
        invalid["center"]["postcode"] = "16802"
        self.assertEqual(self.client.post("/api/hotels/saved", json=invalid).status_code, 400)
        self.assertEqual(self.client.get("/api/hotels/saved", params={"zip_code": "1680"}).status_code, 400)
        with self.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM saved_hotels").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
