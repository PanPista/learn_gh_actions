"""Run the browser UI with deterministic client responses for Playwright."""

import app


def get_country(code: str) -> dict[str, object]:
    return {"data": {"code": code, "name": "United States"}}


def list_countries(page_size: int) -> dict[str, object]:
    return {
        "data": [
            {"code": "US", "name": "United States"},
            {"code": "CA", "name": "Canada"},
        ][:page_size]
    }


app.get_country = get_country
app.list_countries = list_countries

if __name__ == "__main__":
    app.app.run(host=app.HOST, port=app.PORT)
