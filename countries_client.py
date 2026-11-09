"""Client functions for GoREST's public countries endpoints."""

import json
from typing import Any, Optional
from urllib.error import URLError
from urllib.parse import quote, urlencode
from urllib.request import urlopen


BASE_URL = "https://gorest.co.in/public/v3/countries"
PAGE_SIZE = 10
REQUEST_TIMEOUT_SECONDS = 10


class CountriesClientError(Exception):
    """Raised when the GoREST countries API cannot provide a valid response."""


def list_countries(page: Optional[int] = None) -> dict[str, Any]:
    """Return one page of countries and its API pagination metadata."""
    params: dict[str, int] = {"page[size]": PAGE_SIZE}
    if page is not None:
        params["page[number]"] = page

    return _get_json(BASE_URL, params=params)


def get_country(code: str) -> dict[str, Any]:
    """Return the country identified by an ISO 3166-1 alpha-2 code."""
    country_url = f"{BASE_URL}/{quote(code, safe='')}"
    return _get_json(country_url)


def _get_json(
    url: str, *, params: Optional[dict[str, int]] = None
) -> dict[str, Any]:
    if params:
        url = f"{url}?{urlencode(params)}"

    try:
        with urlopen(url, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read())
    except (URLError, TimeoutError, OSError) as error:
        raise CountriesClientError("The GoREST countries API request failed.") from error
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise CountriesClientError(
            "The GoREST countries API returned invalid JSON."
        ) from error
