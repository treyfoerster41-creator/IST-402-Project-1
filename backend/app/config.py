"""Backend-only configuration, independent of the current working directory."""

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(ENV_FILE, override=False)


def geoapify_api_key() -> str:
    """Return the private key for outbound requests only; never log this value."""
    return os.environ.get("GEOAPIFY_API_KEY", "").strip()


def geoapify_configuration_status() -> str:
    return "key is configured" if geoapify_api_key() else "key is not configured"
