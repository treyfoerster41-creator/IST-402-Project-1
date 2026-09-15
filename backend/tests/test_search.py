import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

from backend.app.database import initialize_database
from backend.app.main import app


class ExpediaLiteApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.TemporaryDirectory()
        cls.database_file = Path(cls.temp_dir.name) / "expedia-lite-test.db"
        cls.original_database_path = os.environ.get("EXPEDIA_LITE_DB_PATH")
        os.environ["EXPEDIA_LITE_DB_PATH"] = str(cls.database_file)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        if cls.original_database_path is None:
            os.environ.pop("EXPEDIA_LITE_DB_PATH", None)
        else:
            os.environ["EXPEDIA_LITE_DB_PATH"] = cls.original_database_path
        cls.temp_dir.cleanup()

    def setUp(self):
        if self.database_file.exists():
            self.database_file.unlink()
        initialize_database()

    def create_test_booking(self):
        response = self.client.post("/api/bookings", json={"user_id": "U006", "trip_id": "T001"})
        self.assertEqual(response.status_code, 201)
        return response.json()["booking"]

    def test_boston_returns_the_expected_joined_trip_ids(self):
        response = self.client.get("/api/stays", params={"city": "boston"})
        self.assertEqual(response.status_code, 200)
        stays = response.json()["stays"]
        self.assertEqual([stay["trip_id"] for stay in stays], ["T001", "T002", "T009", "T010"])
        self.assertEqual(stays[0]["hotel_name"], "Harbor Lantern Hotel")
        self.assertEqual(stays[0]["nights"], 2)
        self.assertEqual(stays[0]["stay_price_usd"], 300)

    def test_unknown_city_returns_an_empty_stay_list(self):
        response = self.client.get("/api/stays", params={"city": "Miami"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["stays"], [])

    def test_empty_city_is_a_clear_client_error(self):
        response = self.client.get("/api/stays", params={"city": "   "})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "Enter a city to search.")

    def test_seeded_history_and_empty_history_are_available(self):
        seeded = self.client.get("/api/bookings", params={"user_id": "U001"})
        empty = self.client.get("/api/bookings", params={"user_id": "U006"})
        self.assertEqual([booking["booking_id"] for booking in seeded.json()["bookings"]], ["B002", "B001"])
        self.assertEqual(empty.json()["bookings"], [])

    def test_create_booking_is_saved_after_reinitialization(self):
        booking = self.create_test_booking()
        self.assertEqual(booking["booking_id"], "B007")
        self.assertEqual(booking["status"], "confirmed")
        initialize_database()
        history = self.client.get("/api/bookings", params={"user_id": "U006"}).json()["bookings"]
        self.assertEqual([item["booking_id"] for item in history], ["B007"])

    def test_cancel_keeps_the_booking_in_history(self):
        booking = self.create_test_booking()
        response = self.client.patch(f"/api/bookings/{booking['booking_id']}/cancel")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["booking"]["status"], "cancelled")
        history = self.client.get("/api/bookings", params={"user_id": "U006"}).json()["bookings"]
        self.assertEqual(history[0]["booking_id"], booking["booking_id"])
        self.assertEqual(history[0]["status"], "cancelled")

    def test_delete_removes_a_test_booking_without_reseeding_it(self):
        booking = self.create_test_booking()
        response = self.client.delete(f"/api/bookings/{booking['booking_id']}")
        self.assertEqual(response.status_code, 200)
        initialize_database()
        history = self.client.get("/api/bookings", params={"user_id": "U006"}).json()["bookings"]
        self.assertEqual(history, [])
