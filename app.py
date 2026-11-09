"""Flask browser UI for the GoREST countries client."""

import re

from flask import Flask, render_template, request

from countries_client import CountriesClientError, get_country, list_countries


HOST = "127.0.0.1"
PORT = 8000
MAX_COUNTRIES = 100
COUNTRY_CODE_PATTERN = re.compile(r"[A-Za-z]{2}")

app = Flask(__name__)


def parse_limit(value: str) -> int:
    """Validate a requested number of countries."""
    try:
        limit = int(value)
    except ValueError as error:
        raise ValueError("Enter a whole number.") from error

    if not 1 <= limit <= MAX_COUNTRIES:
        raise ValueError(f"Enter a number from 1 to {MAX_COUNTRIES}.")

    return limit


@app.get("/")
def index() -> str:
    """Render the countries interface and handle its submitted request."""
    code = request.args.get("code", "").strip()
    limit = request.args.get("limit", "").strip()
    result = None
    error = None
    response_section = None

    try:
        if code:
            response_section = "country"
            if not COUNTRY_CODE_PATTERN.fullmatch(code):
                raise ValueError("Enter a two-letter country code.")
            result = get_country(code.upper())
        elif limit:
            response_section = "list"
            result = list_countries(page_size=parse_limit(limit))
    except (CountriesClientError, ValueError) as request_error:
        error = str(request_error)

    return render_template(
        "index.html",
        country_code=code,
        error=error,
        limit=limit or "10",
        max_countries=MAX_COUNTRIES,
        response_section=response_section,
        result=result,
    )


def main() -> None:
    """Start the local UI server."""
    app.run(host=HOST, port=PORT)


if __name__ == "__main__":
    main()
