"""Hotel discovery checks use synthetic locations and mocked provider responses."""

import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from backend.app.geoapify import ZipLookupError
from backend.app.hotel_discovery import (
    HOTEL_LIMIT,
    PLACES_URL,
    REQUEST_TIMEOUT,
    SEARCH_RADIUS_METERS,
    search_nearby_hotels,
)
from backend.app.main import app


SYNTHETIC_KEY = "synthetic-test-key-not-a-real-credential"
CENTER = {
    "postcode": "16802",
    "country_code": "us",
    "latitude": 40.8,
    "longitude": -77.9,
    "locality": "Synthetic Town",
}


def place(place_id="synthetic-place-1", **changes):
    properties = {"place_id": place_id, "name": "Synthetic Hotel", "formatted": "1 Example St"}
    properties.update(changes)
    return {"type": "Feature", "properties": properties, "geometry": {"type": "Point", "coordinates": [-77.91, 40.81]}}


def places_response(features=None, status=200, content=None):
    request = httpx.Request("GET", PLACES_URL)
    if content is not None:
        return httpx.Response(status, content=content, request=request)
    return httpx.Response(status, json={"type": "FeatureCollection", "features": features if features is not None else []}, request=request)


class HotelDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.lookup_patch = patch("backend.app.hotel_discovery.lookup_zip_location", return_value=CENTER)
        self.lookup = self.lookup_patch.start()
        self.addCleanup(self.lookup_patch.stop)
        self.key_patch = patch("backend.app.hotel_discovery.geoapify_api_key", return_value=SYNTHETIC_KEY)
        self.key_patch.start()
        self.addCleanup(self.key_patch.stop)
        self.http_patch = patch("backend.app.hotel_discovery.httpx.get")
        self.http = self.http_patch.start()
        self.addCleanup(self.http_patch.stop)

    def assert_safe_error(self, status):
        with self.assertRaises(ZipLookupError) as caught:
            search_nearby_hotels("16802")
        self.assertEqual(caught.exception.status_code, status)
        self.assertNotIn(SYNTHETIC_KEY, caught.exception.message)
        self.assertNotIn(PLACES_URL, caught.exception.message)
        return caught.exception.message

    def test_exact_zip_center_drives_filtered_hotel_request(self):
        self.http.return_value = places_response([place()])
        result = search_nearby_hotels("16802")
        self.lookup.assert_called_once_with("16802")
        self.http.assert_called_once_with(
            PLACES_URL,
            params={
                "categories": "accommodation.hotel",
                "filter": "circle:-77.9,40.8,5000",
                "bias": "proximity:-77.9,40.8",
                "limit": HOTEL_LIMIT,
                "apiKey": SYNTHETIC_KEY,
            },
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False,
        )
        self.assertEqual(result["center"], CENTER)
        self.assertEqual(result["radius_meters"], SEARCH_RADIUS_METERS)
        self.assertEqual(result["hotels"], [{
            "place_id": "synthetic-place-1", "name": "Synthetic Hotel", "address": "1 Example St",
            "latitude": 40.81, "longitude": -77.91,
        }])
        self.assertNotIn("price", str(result))

    def test_leading_zero_is_forwarded_without_numeric_conversion(self):
        self.lookup.return_value = {**CENTER, "postcode": "02108"}
        self.http.return_value = places_response([])
        result = search_nearby_hotels("02108")
        self.lookup.assert_called_once_with("02108")
        self.assertEqual(result["center"]["postcode"], "02108")

    def test_invalid_or_unresolved_zip_never_calls_places(self):
        for status in (400, 404, 502, 503, 504):
            with self.subTest(status=status):
                self.lookup.side_effect = ZipLookupError(status, "Safe synthetic location failure.")
                self.assert_safe_error(status)
        self.http.assert_not_called()

    def test_empty_success_is_distinct_from_failure(self):
        self.http.return_value = places_response([])
        self.assertEqual(search_nearby_hotels("16802")["hotels"], [])

    def test_missing_optional_fields_are_null_and_duplicate_ids_are_removed(self):
        self.http.return_value = places_response([
            place(name=" ", formatted=None, address_line1=" 10 First ", address_line2="Town"),
            place(name="Duplicate version"),
            place("synthetic-place-2", name=None, formatted=None),
        ])
        hotels = search_nearby_hotels("16802")["hotels"]
        self.assertEqual(len(hotels), 2)
        self.assertIsNone(hotels[0]["name"])
        self.assertEqual(hotels[0]["address"], "10 First, Town")
        self.assertIsNone(hotels[1]["address"])

    def test_unusable_features_are_omitted_but_all_unusable_is_an_error(self):
        bad = place()
        bad["geometry"]["coordinates"] = [-77.9, "not-a-latitude"]
        no_id = place("")
        self.http.return_value = places_response([bad, no_id, place("usable")])
        self.assertEqual([item["place_id"] for item in search_nearby_hotels("16802")["hotels"]], ["usable"])
        self.http.return_value = places_response([bad, no_id])
        self.assertIn("no usable", self.assert_safe_error(502))

    def test_rate_limit_timeout_and_upstream_failures_are_not_empty_results(self):
        self.http.return_value = places_response(status=429)
        self.assertIn("rate-limited", self.assert_safe_error(503))
        self.http.return_value = places_response(status=500)
        self.assert_safe_error(502)
        self.http.side_effect = httpx.TimeoutException(f"{PLACES_URL}?apiKey={SYNTHETIC_KEY}")
        self.assert_safe_error(504)
        self.http.side_effect = None
        self.http.return_value = places_response(content=b"not json")
        self.assert_safe_error(502)

    def test_bad_response_shape_is_a_failure(self):
        self.http.return_value = httpx.Response(200, json={"features": []}, request=httpx.Request("GET", PLACES_URL))
        self.assert_safe_error(502)


class HotelDiscoveryRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.addCleanup(self.client.close)

    def test_route_returns_controller_response(self):
        result = {"center": CENTER, "radius_meters": 5000, "result_limit": 50, "hotels": []}
        with patch("backend.app.main.search_nearby_hotels", return_value=result) as search:
            response = self.client.get("/api/hotels/nearby", params={"zip_code": "02108"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), result)
        search.assert_called_once_with("02108")

    def test_route_preserves_safe_errors(self):
        with patch("backend.app.main.search_nearby_hotels", side_effect=ZipLookupError(404, "No matching U.S. location.")):
            response = self.client.get("/api/hotels/nearby", params={"zip_code": "00000"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No matching U.S. location."})
