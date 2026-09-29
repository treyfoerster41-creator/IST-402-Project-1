"""Live hotel discovery from the exact ZIP point; no SQLite or booking claims."""

import httpx

from .config import geoapify_api_key
from .geoapify import REQUEST_TIMEOUT, ZipLookupError, lookup_zip_location, valid_coordinate

PLACES_URL = "https://api.geoapify.com/v2/places"
SEARCH_RADIUS_METERS = 5000
HOTEL_LIMIT = 50


def optional_text(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def hotel_from_feature(feature: object) -> dict[str, object] | None:
    """Keep only places with a provider ID and usable point geometry."""
    if not isinstance(feature, dict):
        return None
    properties = feature.get("properties")
    geometry = feature.get("geometry")
    if not isinstance(properties, dict) or not isinstance(geometry, dict):
        return None
    place_id = optional_text(properties.get("place_id"))
    coordinates = geometry.get("coordinates")
    if geometry.get("type") != "Point" or not isinstance(coordinates, list) or len(coordinates) < 2:
        return None
    longitude, latitude = coordinates[:2]
    if not place_id or not valid_coordinate(latitude, 90) or not valid_coordinate(longitude, 180):
        return None
    address = optional_text(properties.get("formatted"))
    if not address:
        lines = [optional_text(properties.get(field)) for field in ("address_line1", "address_line2")]
        address = ", ".join(line for line in lines if line) or None
    return {
        "place_id": place_id,
        "name": optional_text(properties.get("name")),
        "address": address,
        "latitude": latitude,
        "longitude": longitude,
    }


def search_nearby_hotels(zip_code: str) -> dict[str, object]:
    """Resolve an exact U.S. ZIP, then request hotels in its 5 km circle."""
    center = lookup_zip_location(zip_code)
    key = geoapify_api_key()
    longitude = center["longitude"]
    latitude = center["latitude"]
    try:
        response = httpx.get(
            PLACES_URL,
            params={
                "categories": "accommodation.hotel",
                "filter": f"circle:{longitude},{latitude},{SEARCH_RADIUS_METERS}",
                "bias": f"proximity:{longitude},{latitude}",
                "limit": HOTEL_LIMIT,
                "apiKey": key,
            },
            timeout=REQUEST_TIMEOUT,
            follow_redirects=False,
        )
        if response.status_code == 429:
            raise ZipLookupError(503, "The hotel service is rate-limited. Please try again later.")
        response.raise_for_status()
        payload = response.json()
    except httpx.TimeoutException:
        raise ZipLookupError(504, "The hotel service timed out. Please try again.") from None
    except httpx.HTTPError:
        raise ZipLookupError(502, "The hotel service could not complete the request. Please try again later.") from None
    except ValueError:
        raise ZipLookupError(502, "The hotel service returned an unreadable response. Please try again later.") from None

    if not isinstance(payload, dict) or payload.get("type") != "FeatureCollection" or not isinstance(payload.get("features"), list):
        raise ZipLookupError(502, "The hotel service returned an unexpected response. Please try again later.")

    features = payload["features"][:HOTEL_LIMIT]
    hotels = []
    seen_ids = set()
    for feature in features:
        hotel = hotel_from_feature(feature)
        if hotel and hotel["place_id"] not in seen_ids:
            hotels.append(hotel)
            seen_ids.add(hotel["place_id"])
    if features and not hotels:
        raise ZipLookupError(502, "The hotel service returned no usable place locations. Please try again later.")
    return {
        "center": center,
        "radius_meters": SEARCH_RADIUS_METERS,
        "result_limit": HOTEL_LIMIT,
        "hotels": hotels,
    }
