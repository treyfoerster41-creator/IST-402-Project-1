"""FastAPI routes for Expedia Lite Part 1."""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from .data import search_stays

app = FastAPI(title="Expedia Lite API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/stays")
def get_stays(city: str = Query(..., description="City to search")) -> dict[str, object]:
    cleaned_city = city.strip()
    if not cleaned_city:
        raise HTTPException(status_code=400, detail="Enter a city to search.")

    return {"city": cleaned_city, "stays": search_stays(cleaned_city)}
