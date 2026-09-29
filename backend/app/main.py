"""FastAPI routes for SQLite bookings and the public ZIP lookup activity."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import geoapify_configuration_status
from .geoapify import ZipLookupError, lookup_zip_location
from .hotel_discovery import search_nearby_hotels
from .database import (
    cancel_booking,
    create_booking,
    delete_booking,
    initialize_database,
    list_bookings,
    list_users,
    search_stays,
)

app = FastAPI(title="Expedia Lite API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["*"],
)


class BookingRequest(BaseModel):
    user_id: str
    trip_id: str


@app.on_event("startup")
def startup() -> None:
    initialize_database()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "geoapify": geoapify_configuration_status()}


def zip_location_response(zip_code: str) -> dict[str, object]:
    try:
        return lookup_zip_location(zip_code)
    except ZipLookupError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from None


@app.get("/api/demo/zip-location")
def demo_zip_location() -> dict[str, object]:
    return zip_location_response("16802")


@app.get("/api/zip-location")
def get_zip_location(zip_code: str = Query("", description="Five-digit U.S. ZIP code")) -> dict[str, object]:
    return zip_location_response(zip_code)


@app.get("/api/hotels/nearby")
def get_nearby_hotels(zip_code: str = Query("", description="Five-digit U.S. ZIP code")) -> dict[str, object]:
    try:
        return search_nearby_hotels(zip_code)
    except ZipLookupError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from None


@app.get("/api/stays")
def get_stays(city: str = Query(..., description="City to search")) -> dict[str, object]:
    cleaned_city = city.strip()
    if not cleaned_city:
        raise HTTPException(status_code=400, detail="Enter a city to search.")
    return {"city": cleaned_city, "stays": search_stays(cleaned_city)}


@app.get("/api/users")
def get_users() -> dict[str, object]:
    return {"users": list_users()}


@app.get("/api/bookings")
def get_bookings(user_id: str = Query(..., description="Demo traveler ID")) -> dict[str, object]:
    if not any(user["user_id"] == user_id for user in list_users()):
        raise HTTPException(status_code=404, detail="Choose a valid demo traveler.")
    return {"user_id": user_id, "bookings": list_bookings(user_id)}


@app.post("/api/bookings", status_code=201)
def post_booking(request: BookingRequest) -> dict[str, object]:
    booking = create_booking(request.user_id.strip(), request.trip_id.strip())
    if booking is None:
        raise HTTPException(status_code=400, detail="Choose a valid traveler and offered stay.")
    return {"booking": booking}


@app.patch("/api/bookings/{booking_id}/cancel")
def patch_booking_cancel(booking_id: str) -> dict[str, object]:
    booking = cancel_booking(booking_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found.")
    return {"booking": booking}


@app.delete("/api/bookings/{booking_id}")
def remove_booking(booking_id: str) -> dict[str, str]:
    if not delete_booking(booking_id):
        raise HTTPException(status_code=404, detail="Booking not found.")
    return {"message": f"Booking {booking_id} was deleted."}
