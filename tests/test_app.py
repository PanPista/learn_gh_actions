import unittest
from unittest.mock import patch

import app


class AppTests(unittest.TestCase):
    def test_parse_limit_accepts_values_in_range(self):
        self.assertEqual(app.parse_limit("25"), 25)

    def test_parse_limit_rejects_values_outside_allowed_range(self):
        for value in ("0", "101", "three"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    app.parse_limit(value)

    def setUp(self):
        app.app.config["TESTING"] = True
        self.client = app.app.test_client()

    @patch("app.get_country", return_value={"name": "United States"})
    def test_country_response_is_rendered_in_country_form(self, mock_get_country):
        page = self.client.get("/?code=US").get_data(as_text=True)

        response_position = page.index("United States")
        self.assertLess(response_position, page.index('<form method="get">', response_position))
        mock_get_country.assert_called_once_with("US")

    @patch("app.list_countries", return_value={"data": []})
    def test_list_response_is_rendered_in_list_form(self, mock_list_countries):
        page = self.client.get("/?limit=10").get_data(as_text=True)

        response_position = page.index('"data"')
        self.assertGreater(response_position, page.rindex('<form method="get">'))
        mock_list_countries.assert_called_once_with(page_size=10)

    @patch("app.get_country", return_value={"name": "<unsafe>"})
    def test_template_escapes_user_input_and_result(self, mock_get_country):
        page = self.client.get('/?code=<script>alert("x")</script>').get_data(
            as_text=True
        )

        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)
        mock_get_country.assert_not_called()
