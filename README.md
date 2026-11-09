# GoREST countries client

A small reusable Python client for GoREST's public v3 country endpoints. It
uses only the Python standard library.

## Use

```python
from countries_client import CountriesClientError, get_country, list_countries

try:
    countries_page = list_countries(page=2, page_size=25)
    country_code = countries_page["data"][0]["code"]  # The caller selects a code.
    country = get_country(country_code)
except CountriesClientError as error:
    print(f"Could not retrieve country data: {error}")
```

`list_countries()` returns the full decoded list response, including `data` and
`meta`. `get_country(code)` returns the full decoded country object. HTTP,
network, timeout, and invalid-JSON failures raise `CountriesClientError`.

## Browser UI

Start the local interface:

```bash
python3 app.py
```

Then open http://127.0.0.1:8000. You can enter a two-letter country code or
choose how many countries (1-100) to request.

## Tests

Run the Python unit tests:

```bash
python3 -m unittest discover -s tests
```

### End-to-end UI tests

The Playwright tests cover both country endpoints through the browser UI with
deterministic client responses, so they do not call the live GoREST API.

Install the JavaScript dependencies and Chromium once:

```bash
npm ci
npx playwright install chromium
```

Run the UI tests:

```bash
npm run test:ui
```
