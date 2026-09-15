"""SQLite storage, one-time CSV seeding, and query helpers for Expedia Lite."""

from __future__ import annotations

import csv
import os
import sqlite3
from contextlib import contextmanager
from datetime import date
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_DATABASE_PATH = DATA_DIR / "expedia_lite.db"


def database_path() -> Path:
    """Return the local database path, allowing an isolated path for tests."""
    return Path(os.environ.get("EXPEDIA_LITE_DB_PATH", DEFAULT_DATABASE_PATH))


def read_csv(filename: str) -> list[dict[str, str]]:
    """Read a supplied CSV file without treating its UTF-8 BOM as a header character."""
    with (DATA_DIR / filename).open(encoding="utf-8-sig", newline="") as source:
        return list(csv.DictReader(source))


def connection() -> sqlite3.Connection:
    """Open a SQLite connection that returns columns by name and enforces foreign keys."""
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


@contextmanager
def database_session():
    """Commit a database operation and always close its SQLite connection."""
    db = connection()
    try:
        yield db
        db.commit()
    finally:
        db.close()


def initialize_database() -> None:
    """Create tables and seed the supplied records exactly once for each database file."""
    with database_session() as db:
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS app_metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS hotels (
                hotel_id TEXT PRIMARY KEY,
                hotel_name TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                nightly_rate_usd INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                display_name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS trips (
                trip_id TEXT PRIMARY KEY,
                hotel_id TEXT NOT NULL REFERENCES hotels(hotel_id),
                trip_name TEXT NOT NULL,
                check_in TEXT NOT NULL,
                check_out TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS bookings (
                booking_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES users(user_id),
                trip_id TEXT NOT NULL REFERENCES trips(trip_id),
                booked_on TEXT NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('confirmed', 'cancelled'))
            );
            """
        )
        seeded = db.execute(
            "SELECT value FROM app_metadata WHERE key = 'csv_seed_v1'"
        ).fetchone()
        if seeded:
            return

        db.executemany(
            """
            INSERT INTO hotels (hotel_id, hotel_name, city, state, nightly_rate_usd)
            VALUES (:hotel_id, :hotel_name, :city, :state, :nightly_rate_usd)
            """,
            read_csv("hotels.csv"),
        )
        db.executemany(
            "INSERT INTO users (user_id, display_name) VALUES (:user_id, :display_name)",
            read_csv("users.csv"),
        )
        db.executemany(
            """
            INSERT INTO trips (trip_id, hotel_id, trip_name, check_in, check_out)
            VALUES (:trip_id, :hotel_id, :trip_name, :check_in, :check_out)
            """,
            read_csv("trips.csv"),
        )
        db.executemany(
            """
            INSERT INTO bookings (booking_id, user_id, trip_id, booked_on, status)
            VALUES (:booking_id, :user_id, :trip_id, :booked_on, :status)
            """,
            read_csv("bookings.csv"),
        )
        db.execute(
            "INSERT INTO app_metadata (key, value) VALUES ('csv_seed_v1', ?)",
            (date.today().isoformat(),),
        )


STAY_SELECT = """
    SELECT trips.trip_id, trips.trip_name, hotels.hotel_name, hotels.city, hotels.state,
           trips.check_in, trips.check_out, hotels.nightly_rate_usd,
           CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER) AS nights,
           CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER)
             * hotels.nightly_rate_usd AS stay_price_usd
    FROM trips
    JOIN hotels ON hotels.hotel_id = trips.hotel_id
"""


def search_stays(city: str) -> list[dict[str, object]]:
    """Return SQLite-backed stays in a city, matching without regard to case."""
    initialize_database()
    with database_session() as db:
        rows = db.execute(
            STAY_SELECT
            + " WHERE lower(hotels.city) = lower(?) ORDER BY trips.check_in, trips.trip_id",
            (city.strip(),),
        ).fetchall()
    return [dict(row) for row in rows]


def list_users() -> list[dict[str, str]]:
    initialize_database()
    with database_session() as db:
        rows = db.execute("SELECT user_id, display_name FROM users ORDER BY user_id").fetchall()
    return [dict(row) for row in rows]


def next_booking_id(db: sqlite3.Connection) -> str:
    """Create the next B-prefixed booking ID without changing any supplied IDs."""
    rows = db.execute("SELECT booking_id FROM bookings WHERE booking_id GLOB 'B[0-9]*'").fetchall()
    highest = max((int(row["booking_id"][1:]) for row in rows), default=0)
    return f"B{highest + 1:03d}"


def booking_details(booking_id: str) -> dict[str, object] | None:
    initialize_database()
    with database_session() as db:
        row = db.execute(
            """
            SELECT bookings.booking_id, bookings.user_id, users.display_name, bookings.trip_id,
                   bookings.booked_on, bookings.status, trips.trip_name, hotels.hotel_name,
                   hotels.city, hotels.state, trips.check_in, trips.check_out,
                   CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER) AS nights,
                   hotels.nightly_rate_usd,
                   CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER)
                     * hotels.nightly_rate_usd AS stay_price_usd
            FROM bookings
            JOIN users ON users.user_id = bookings.user_id
            JOIN trips ON trips.trip_id = bookings.trip_id
            JOIN hotels ON hotels.hotel_id = trips.hotel_id
            WHERE bookings.booking_id = ?
            """,
            (booking_id,),
        ).fetchone()
    return dict(row) if row else None


def list_bookings(user_id: str) -> list[dict[str, object]]:
    initialize_database()
    with database_session() as db:
        rows = db.execute(
            """
            SELECT bookings.booking_id, bookings.user_id, users.display_name, bookings.trip_id,
                   bookings.booked_on, bookings.status, trips.trip_name, hotels.hotel_name,
                   hotels.city, hotels.state, trips.check_in, trips.check_out,
                   CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER) AS nights,
                   hotels.nightly_rate_usd,
                   CAST(julianday(trips.check_out) - julianday(trips.check_in) AS INTEGER)
                     * hotels.nightly_rate_usd AS stay_price_usd
            FROM bookings
            JOIN users ON users.user_id = bookings.user_id
            JOIN trips ON trips.trip_id = bookings.trip_id
            JOIN hotels ON hotels.hotel_id = trips.hotel_id
            WHERE bookings.user_id = ?
            ORDER BY bookings.booked_on DESC, bookings.booking_id DESC
            """,
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def create_booking(user_id: str, trip_id: str) -> dict[str, object] | None:
    initialize_database()
    with database_session() as db:
        user_exists = db.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,)).fetchone()
        trip_exists = db.execute("SELECT 1 FROM trips WHERE trip_id = ?", (trip_id,)).fetchone()
        if not user_exists or not trip_exists:
            return None
        booking_id = next_booking_id(db)
        db.execute(
            """
            INSERT INTO bookings (booking_id, user_id, trip_id, booked_on, status)
            VALUES (?, ?, ?, ?, 'confirmed')
            """,
            (booking_id, user_id, trip_id, date.today().isoformat()),
        )
    return booking_details(booking_id)


def cancel_booking(booking_id: str) -> dict[str, object] | None:
    initialize_database()
    with database_session() as db:
        cursor = db.execute(
            "UPDATE bookings SET status = 'cancelled' WHERE booking_id = ?", (booking_id,)
        )
        if cursor.rowcount == 0:
            return None
    return booking_details(booking_id)


def delete_booking(booking_id: str) -> bool:
    initialize_database()
    with connection() as db:
        cursor = db.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
    return cursor.rowcount > 0
