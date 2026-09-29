"""ZIP geocoding controller. No database access or credentials in responses."""

import logging
import math
import re

import httpx

from .config import geoapify_api_key

GEOCODING_URL = "https://api.geoapify.com/v1/geocode/search"
REQUEST_TIMEOUT = 10.0

# HTTPX's INFO request log includes the credential-bearing provider URL.
# Do not enable HTTP client debug logging in this credential-owning backend.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class ZipLookupError(Exception):
    """Only constant, credential-free messages are allowed at this boundary."""

    def __init__(self, status_code: int, message: str):
        super().__init__(message)
        self.status_code = status_code
        self.message = message


def valid_coordinate(value: object, limit: float) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and -limit <= value <= limit
    )


def lookup_zip_location(zip_code: str) -> dict[str, object]:
    """Resolve exactly one five-digit U.S. ZIP or raise a safe ZipLookupError."""
    postcode = zip_code.strip()
    if not re.fullmatch(r"[0-9]{5}", postcode):
        raise ZipLookupError(400, "Enter a five-digit U.S. ZIP code, such as 16802.")

    key = geoapify_api_key()
    if not key:
        raise ZipLookupError(503, "Geoapify key is not configured. Set the backend .env key and restart the backend.")

    try:
        response = httpx.get(
            GEOCODING_URL,
            params={
                "postcode": postcode,
                "type": "postcode",
                "filter": "countrycode:us",
                "format": "json",
                "apiKey": key,
            },
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False,
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.TimeoutException:
        raise ZipLookupError(504, "The location service timed out. Please try again.") from None
    except httpx.HTTPError:
        raise ZipLookupError(502, "The location service could not complete the request. Try again later or check the backend key configuration.") from None
    except ValueError:
        raise ZipLookupError(502, "The location service returned an unreadable response. Please try again later.") from None

    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ZipLookupError(502, "The location service returned an unexpected response. Please try again later.")

    invalid_match = False
    for result in payload["results"]:
        if not isinstance(result, dict):
            raise ZipLookupError(502, "The location service returned an unexpected response. Please try again later.")
        if result.get("postcode") != postcode or result.get("country_code") != "us":
            continue
        latitude, longitude = result.get("lat"), result.get("lon")
        if not valid_coordinate(latitude, 90) or not valid_coordinate(longitude, 180):
            invalid_match = True
            continue
        locality = next(
            (result[field].strip() for field in ("city", "town", "village")
             if isinstance(result.get(field), str) and result[field].strip()),
            None,
        )
        return {
            "postcode": postcode,
            "country_code": "us",
            "latitude": latitude,
            "longitude": longitude,
            "locality": locality,
        }

    if invalid_match:
        raise ZipLookupError(502, "The location service returned invalid coordinates. Please try again later.")
    raise ZipLookupError(404, "No matching U.S. location was found for this ZIP code. Try another ZIP.")
