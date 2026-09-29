"""ZIP activity checks use synthetic keys and mocked HTTP, never Geoapify."""

import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

import httpx
from fastapi.testclient import TestClient

from backend.app import config
from backend.app.geoapify import (
    GEOCODING_URL,
    REQUEST_TIMEOUT,
    ZipLookupError,
    lookup_zip_location,
)
from backend.app.main import app


SYNTHETIC_KEY = "synthetic-test-key-not-a-real-credential"
SYNTHETIC_LOCATION = {
    "postcode": "16802",
    "country_code": "us",
    "latitude": 40.8,
    "longitude": -77.9,
    "locality": "Synthetic University Park",
}


def provider_result(**changes):
    """A labeled fixture; these coordinates are not evidence of a live lookup."""
    result = {
        "postcode": "16802",
        "country_code": "us",
        "lat": 40.8,
        "lon": -77.9,
        "city": "Synthetic University Park",
    }
    result.update(changes)
    return result


def provider_response(payload=None, status=200, content=None):
    request = httpx.Request("GET", GEOCODING_URL)
    if content is not None:
        return httpx.Response(status, content=content, request=request)
    return httpx.Response(status, json=payload, request=request)


class GeoapifyConfigurationTests(unittest.TestCase):
    def test_dotenv_uses_explicit_project_root_and_preserves_environment(self):
        # Re-execute only the helper with a mocked loader, without reading .env.
        helper_path = Path(config.__file__).resolve()
        with patch("dotenv.load_dotenv") as load_dotenv:
            runpy.run_path(str(helper_path))
        load_dotenv.assert_called_once_with(helper_path.parents[2] / ".env", override=False)

    def test_absent_empty_and_whitespace_keys_are_not_configured(self):
        for value in (None, "", "   \t\n"):
            with self.subTest(value=value), patch.dict(os.environ):
                if value is None:
                    os.environ.pop("GEOAPIFY_API_KEY", None)
                else:
                    os.environ["GEOAPIFY_API_KEY"] = value
                self.assertEqual(config.geoapify_api_key(), "")
                self.assertEqual(config.geoapify_configuration_status(), "key is not configured")

    def test_present_key_is_trimmed_and_only_status_is_reported(self):
        with patch.dict(os.environ, {"GEOAPIFY_API_KEY": f"  {SYNTHETIC_KEY}  "}):
            self.assertEqual(config.geoapify_api_key(), SYNTHETIC_KEY)
            self.assertEqual(config.geoapify_configuration_status(), "key is configured")


class GeoapifyControllerTests(unittest.TestCase):
    def setUp(self):
        self.key_patch = patch("backend.app.geoapify.geoapify_api_key", return_value=SYNTHETIC_KEY)
        self.key = self.key_patch.start()
        self.addCleanup(self.key_patch.stop)
        self.http_patch = patch("backend.app.geoapify.httpx.get")
        self.http = self.http_patch.start()
        self.addCleanup(self.http_patch.stop)

    def assert_lookup_error(self, expected_status, zip_code="16802"):
        with self.assertRaises(ZipLookupError) as caught:
            lookup_zip_location(zip_code)
        error = caught.exception
        self.assertEqual(error.status_code, expected_status)
        self.assertNotIn(SYNTHETIC_KEY, error.message)
        self.assertNotIn(GEOCODING_URL, error.message)
        self.assertNotIn("apiKey", error.message)
        return error.message

    def test_success_uses_required_provider_parameters_and_small_response(self):
        self.http.return_value = provider_response({"results": [provider_result()]})
        self.assertEqual(lookup_zip_location(" 16802 "), SYNTHETIC_LOCATION)
        self.http.assert_called_once_with(
            GEOCODING_URL,
            params={
                "postcode": "16802",
                "type": "postcode",
                "filter": "countrycode:us",
                "format": "json",
                "apiKey": SYNTHETIC_KEY,
            },
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False,
        )
        self.assertGreater(REQUEST_TIMEOUT, 0)
        self.assertLessEqual(REQUEST_TIMEOUT, 30)

    def test_leading_zero_survives_request_and_response(self):
        self.http.return_value = provider_response({"results": [provider_result(postcode="02108")]})
        result = lookup_zip_location("02108")
        self.assertEqual(result["postcode"], "02108")
        self.assertEqual(self.http.call_args.kwargs["params"]["postcode"], "02108")

    def test_invalid_input_does_not_request_provider_or_key(self):
        for value in (
            "", "   ", "1680", "168020", "16802-1234", "abcde", "168 2",
            "\uff11\uff16\uff18\uff10\uff12", "\u0661\u0666\u0668\u0660\u0662",
        ):
            with self.subTest(zip_code=value):
                self.assert_lookup_error(400, value)
        self.http.assert_not_called()
        self.key.assert_not_called()

    def test_missing_key_does_not_request_provider(self):
        self.key.return_value = ""
        self.assertIn("not configured", self.assert_lookup_error(503))
        self.http.assert_not_called()

    def test_empty_results_and_unrelated_locations_are_unresolved(self):
        for results in ([], [provider_result(postcode="16801")], [provider_result(country_code="ca")]):
            with self.subTest(results=results):
                self.http.return_value = provider_response({"results": results})
                self.assertIn("No matching", self.assert_lookup_error(404))

    def test_correct_match_can_follow_unrelated_result(self):
        self.http.return_value = provider_response({
            "results": [provider_result(postcode="16801"), provider_result()],
        })
        self.assertEqual(lookup_zip_location("16802"), SYNTHETIC_LOCATION)

    def test_invalid_coordinates_are_rejected(self):
        for field, value in (
            ("lat", None), ("lon", None), ("lat", "40.8"), ("lon", "-77.9"),
            ("lat", True), ("lon", False), ("lat", 91), ("lat", -91),
            ("lon", 181), ("lon", -181),
        ):
            with self.subTest(field=field, value=value):
                self.http.return_value = provider_response({"results": [provider_result(**{field: value})]})
                self.assertIn("invalid coordinates", self.assert_lookup_error(502))

    def test_nonfinite_and_missing_coordinates_are_rejected(self):
        # Mock JSON decoding directly because strict JSON does not encode NaN.
        for value in (float("nan"), float("inf"), -float("inf")):
            with self.subTest(value=value):
                self.http.return_value.json.return_value = {"results": [provider_result(lat=value)]}
                self.assert_lookup_error(502)
        for field in ("lat", "lon"):
            result = provider_result()
            result.pop(field)
            self.http.return_value.json.return_value = {"results": [result]}
            self.assert_lookup_error(502)

    def test_locality_is_optional_and_uses_available_town_or_village(self):
        for changes, expected in (
            ({"city": None, "town": "  Synthetic Town  "}, "Synthetic Town"),
            ({"city": " ", "village": "Synthetic Village"}, "Synthetic Village"),
            ({"city": None}, None),
        ):
            with self.subTest(changes=changes):
                self.http.return_value = provider_response({"results": [provider_result(**changes)]})
                self.assertEqual(lookup_zip_location("16802")["locality"], expected)

    def test_timeout_and_transport_failures_hide_raw_error_text(self):
        secret_url = f"{GEOCODING_URL}?apiKey={SYNTHETIC_KEY}"
        for exception, status in (
            (httpx.TimeoutException(secret_url), 504),
            (httpx.ConnectError(secret_url), 502),
        ):
            with self.subTest(status=status):
                self.http.side_effect = exception
                self.assert_lookup_error(status)

    def test_redirect_and_provider_error_statuses_are_safe_failures(self):
        for status in (301, 401, 403, 429, 500):
            with self.subTest(status=status):
                self.http.return_value = provider_response({"message": SYNTHETIC_KEY}, status=status)
                self.assert_lookup_error(502)

    def test_malformed_json_is_a_safe_provider_failure(self):
        self.http.return_value = provider_response(content=b"not-json")
        self.assertIn("unreadable", self.assert_lookup_error(502))

    def test_unexpected_payload_schema_is_a_safe_provider_failure(self):
        for payload in ([], None, {}, {"results": {}}, {"results": [None]}, {"results": ["invalid"]}):
            with self.subTest(payload=payload):
                self.http.return_value = provider_response(payload)
                self.assert_lookup_error(502)


class ZipLookupRouteTests(unittest.TestCase):
    def setUp(self):
        # No lifespan context: these route tests must never initialize SQLite.
        self.client = TestClient(app)
        self.addCleanup(self.client.close)
        self.http_patch = patch("backend.app.geoapify.httpx.get")
        self.http = self.http_patch.start()
        self.addCleanup(self.http_patch.stop)
        self.key_patch = patch("backend.app.geoapify.geoapify_api_key", return_value=SYNTHETIC_KEY)
        self.key_patch.start()
        self.addCleanup(self.key_patch.stop)

    def test_fixed_demo_passes_16802_to_controller(self):
        with patch("backend.app.main.lookup_zip_location", return_value=SYNTHETIC_LOCATION) as lookup:
            response = self.client.get("/api/demo/zip-location")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), SYNTHETIC_LOCATION)
        lookup.assert_called_once_with("16802")
        self.http.assert_not_called()

    def test_entered_zip_is_forwarded_as_text(self):
        location = {**SYNTHETIC_LOCATION, "postcode": "02108"}
        with patch("backend.app.main.lookup_zip_location", return_value=location) as lookup:
            response = self.client.get("/api/zip-location", params={"zip_code": "02108"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), location)
        lookup.assert_called_once_with("02108")
        self.http.assert_not_called()

    def test_missing_or_invalid_entered_zip_is_clear_without_http_request(self):
        for params in ({}, {"zip_code": ""}, {"zip_code": "invalid"}):
            with self.subTest(params=params):
                response = self.client.get("/api/zip-location", params=params)
                self.assertEqual(response.status_code, 400)
                self.assertIn("five-digit", response.json()["detail"])
        self.http.assert_not_called()

    def test_controller_error_status_and_message_are_preserved(self):
        for status in (400, 404, 502, 503, 504):
            for endpoint in ("/api/demo/zip-location", "/api/zip-location?zip_code=16802"):
                with self.subTest(status=status, endpoint=endpoint):
                    error = ZipLookupError(status, "Safe synthetic failure.")
                    with patch("backend.app.main.lookup_zip_location", side_effect=error):
                        response = self.client.get(endpoint)
                    self.assertEqual(response.status_code, status)
                    self.assertEqual(response.json(), {"detail": "Safe synthetic failure."})
        self.http.assert_not_called()

    def test_health_retains_status_and_exposes_only_key_presence(self):
        for key, expected in (("", "key is not configured"), (SYNTHETIC_KEY, "key is configured")):
            with self.subTest(expected=expected), patch("backend.app.config.geoapify_api_key", return_value=key):
                response = self.client.get("/api/health")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json(), {"status": "ok", "geoapify": expected})
                self.assertNotIn(SYNTHETIC_KEY, response.text)
        self.http.assert_not_called()


if __name__ == "__main__":
    unittest.main()
