"""Local copies of Geoapify hotel places and fictional dated classroom values."""

from __future__ import annotations

import re
from datetime import date, timedelta

from .database import database_session, initialize_database
from .geoapify import valid_coordinate
from .hotel_discovery import HOTEL_LIMIT, SEARCH_RADIUS_METERS

DEMO_DATES = tuple((date(2026, 10, 10) + timedelta(days=day)).isoformat() for day in range(5))


def validate_zip(zip_code: object) -> str:
    if not isinstance(zip_code, str) or not re.fullmatch(r"[0-9]{5}", zip_code):
        raise ValueError("Enter a five-digit U.S. ZIP code.")
    return zip_code


def optional_text(value: object, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"Hotel {field} must be text or missing.")
    return value.strip() or None


def validate_save_request(
    zip_code: object, center: object, hotel: object
) -> tuple[str, dict[str, object], dict[str, object]]:
    """Accept only the small, safe hotel and exact-ZIP shapes used by Part 1."""
    postcode = validate_zip(zip_code)
    if not isinstance(center, dict) or center.get("postcode") != postcode or center.get("country_code") != "us":
        raise ValueError("The saved location must match the searched U.S. ZIP code.")
    if not valid_coordinate(center.get("latitude"), 90) or not valid_coordinate(center.get("longitude"), 180):
        raise ValueError("The searched ZIP location needs valid coordinates.")
    locality = optional_text(center.get("locality"), "locality")

    if not isinstance(hotel, dict):
        raise ValueError("Choose a returned hotel place to save.")
    hotel_id = hotel.get("place_id")
    if not isinstance(hotel_id, str) or not hotel_id.strip() or hotel_id != hotel_id.strip():
        raise ValueError("The hotel needs a valid provider place ID.")
    if not valid_coordinate(hotel.get("latitude"), 90) or not valid_coordinate(hotel.get("longitude"), 180):
        raise ValueError("The hotel needs valid coordinates.")
    saved_hotel = {
        "hotel_id": hotel_id,
        "name": optional_text(hotel.get("name"), "name"),
        "address": optional_text(hotel.get("address"), "address"),
        "latitude": hotel["latitude"],
        "longitude": hotel["longitude"],
    }
    saved_center = {
        "postcode": postcode,
        "country_code": "us",
        "locality": locality,
        "latitude": center["latitude"],
        "longitude": center["longitude"],
    }
    return postcode, saved_center, saved_hotel


def saved_hotels_for_zip(zip_code: str) -> dict[str, object]:
    """Read saved places and current nightly rows directly from SQLite each time."""
    postcode = validate_zip(zip_code)
    initialize_database()
    with database_session() as db:
        saved_ids = [row["hotel_id"] for row in db.execute(
            "SELECT hotel_id FROM saved_hotels ORDER BY hotel_id"
        )]
        rows = db.execute(
            """
            SELECT h.hotel_id, h.name, h.address, h.latitude, h.longitude,
                   z.locality, z.center_latitude, z.center_longitude
            FROM saved_hotels AS h
            JOIN saved_hotel_zips AS z ON z.hotel_id = h.hotel_id
            WHERE z.zip_code = ?
            ORDER BY coalesce(h.name, ''), h.hotel_id
            """,
            (postcode,),
        ).fetchall()
        hotels = []
        for row in rows:
            nights = db.execute(
                """
                SELECT stay_date, nightly_rate_cents, rooms_available
                FROM demo_hotel_nights WHERE hotel_id = ? ORDER BY stay_date
                """,
                (row["hotel_id"],),
            ).fetchall()
            hotels.append({
                "place_id": row["hotel_id"],
                "name": row["name"],
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "demo_nights": [dict(night) for night in nights],
            })
    center = None
    if rows:
        center = {
            "postcode": postcode,
            "country_code": "us",
            "locality": rows[0]["locality"],
            "latitude": rows[0]["center_latitude"],
            "longitude": rows[0]["center_longitude"],
        }
    return {
        "center": center,
        "radius_meters": SEARCH_RADIUS_METERS,
        "result_limit": HOTEL_LIMIT,
        "hotels": hotels,
        "saved_ids": saved_ids,
    }


def save_api_hotel(zip_code: object, center: object, hotel: object) -> dict[str, object]:
    postcode, saved_center, saved_hotel = validate_save_request(zip_code, center, hotel)
    initialize_database()
    with database_session() as db:
        created = db.execute(
            """
            INSERT OR IGNORE INTO saved_hotels (hotel_id, name, address, latitude, longitude)
            VALUES (:hotel_id, :name, :address, :latitude, :longitude)
            """,
            saved_hotel,
        ).rowcount > 0
        db.execute(
            """
            INSERT OR IGNORE INTO saved_hotel_zips
                (hotel_id, zip_code, locality, center_latitude, center_longitude)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                saved_hotel["hotel_id"], postcode, saved_center["locality"],
                saved_center["latitude"], saved_center["longitude"],
            ),
        )
        db.executemany(
            """
            INSERT OR IGNORE INTO demo_hotel_nights (hotel_id, stay_date)
            VALUES (?, ?)
            """,
            [(saved_hotel["hotel_id"], stay_date) for stay_date in DEMO_DATES],
        )
    result = saved_hotels_for_zip(postcode)
    stored_hotel = next(item for item in result["hotels"] if item["place_id"] == saved_hotel["hotel_id"])
    return {"hotel": stored_hotel, "created": created}


def remove_saved_hotel(hotel_id: str) -> bool:
    """Delete one provider place; foreign keys cascade to ZIPs and nightly rows."""
    if not hotel_id:
        return False
    initialize_database()
    with database_session() as db:
        deleted = db.execute("DELETE FROM saved_hotels WHERE hotel_id = ?", (hotel_id,)).rowcount
    return deleted > 0
