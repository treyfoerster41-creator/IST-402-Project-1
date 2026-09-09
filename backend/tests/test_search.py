import unittest

from fastapi.testclient import TestClient

from backend.app.main import app


class CitySearchTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

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
