"""CSV loading and hotel/trip join logic for Part 1."""

from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def read_csv(filename: str) -> list[dict[str, str]]:
    """Read a supplied UTF-8 CSV file, handling its optional byte-order mark."""
    with (DATA_DIR / filename).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def search_stays(city: str) -> list[dict[str, object]]:
    """Return trips whose joined hotel city matches city, case-insensitively."""
    normalized_city = city.strip().casefold()
    if not normalized_city:
        return []

    hotels_by_id = {hotel["hotel_id"]: hotel for hotel in read_csv("hotels.csv")}
    stays: list[dict[str, object]] = []

    for trip in read_csv("trips.csv"):
        hotel = hotels_by_id.get(trip["hotel_id"])
        if hotel is None or hotel["city"].casefold() != normalized_city:
            continue

        check_in = date.fromisoformat(trip["check_in"])
        check_out = date.fromisoformat(trip["check_out"])
        nights = (check_out - check_in).days
        nightly_rate = int(hotel["nightly_rate_usd"])
        stays.append(
            {
                "trip_id": trip["trip_id"],
                "trip_name": trip["trip_name"],
                "hotel_name": hotel["hotel_name"],
                "city": hotel["city"],
                "state": hotel["state"],
                "check_in": trip["check_in"],
                "check_out": trip["check_out"],
                "nights": nights,
                "nightly_rate_usd": nightly_rate,
                "stay_price_usd": nights * nightly_rate,
            }
        )

    return stays

