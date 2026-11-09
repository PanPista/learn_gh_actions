# GoREST countries client

A small reusable Python client for GoREST's public v3 country endpoints. It
uses only the Python standard library.

## Use

```python
from countries_client import CountriesClientError, get_country, list_countries

try:
    countries_page = list_countries(page=2)  # Optional; requests 10 countries per page.
    country_code = countries_page["data"][0]["code"]  # The caller selects a code.
    country = get_country(country_code)
except CountriesClientError as error:
    print(f"Could not retrieve country data: {error}")
```

`list_countries()` returns the full decoded list response, including `data` and
`meta`. `get_country(code)` returns the full decoded country object. HTTP,
network, timeout, and invalid-JSON failures raise `CountriesClientError`.

## Test

```bash
python3 -m unittest discover -s tests
```
