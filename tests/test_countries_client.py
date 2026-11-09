import json
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import URLError

import countries_client


class CountriesClientTests(unittest.TestCase):
    def test_list_countries_returns_response_with_pagination_metadata(self):
        expected_response = {
            "data": [{"code": "IN", "name": "India"}],
            "meta": {"has_more": True, "next_cursor": "next-page"},
        }
        response = MagicMock()
        response.read.return_value = json.dumps(expected_response).encode()

        with patch("countries_client.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = response

            self.assertEqual(countries_client.list_countries(page=2), expected_response)

        mock_urlopen.assert_called_once_with(
            f"{countries_client.BASE_URL}?page%5Bsize%5D=10&page%5Bnumber%5D=2",
            timeout=countries_client.REQUEST_TIMEOUT_SECONDS,
        )

    def test_list_countries_uses_requested_page_size(self):
        response = MagicMock()
        response.read.return_value = b'{"data": []}'

        with patch("countries_client.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = response

            countries_client.list_countries(page_size=25)

        mock_urlopen.assert_called_once_with(
            f"{countries_client.BASE_URL}?page%5Bsize%5D=25",
            timeout=countries_client.REQUEST_TIMEOUT_SECONDS,
        )

    def test_list_countries_rejects_non_positive_page_size(self):
        with self.assertRaises(ValueError):
            countries_client.list_countries(page_size=0)

    def test_get_country_returns_the_selected_country(self):
        expected_response = {"code": "IN", "name": "India", "region": "Asia"}
        response = MagicMock()
        response.read.return_value = json.dumps(expected_response).encode()

        with patch("countries_client.urlopen") as mock_urlopen:
            mock_urlopen.return_value.__enter__.return_value = response

            self.assertEqual(countries_client.get_country("IN"), expected_response)

        mock_urlopen.assert_called_once_with(
            f"{countries_client.BASE_URL}/IN",
            timeout=countries_client.REQUEST_TIMEOUT_SECONDS,
        )

    def test_list_countries_wraps_request_errors(self):
        with patch(
            "countries_client.urlopen", side_effect=URLError("request timed out")
        ):
            with self.assertRaises(countries_client.CountriesClientError) as error:
                countries_client.list_countries()

        self.assertIsInstance(error.exception.__cause__, URLError)
