# pylint: disable=pointless-string-statement
"""Python file of unit tests"""
import unittest
from unittest.mock import MagicMock, patch
from app import len_bool_helper, login_helper
from spotify import spotify_access_token_call, spotify_api_image


class CodeTests(unittest.TestCase):
    """python testing class"""

    def test_len_bool_helper(self):
        """Length of fields in signup helper test"""
        user_name_len = 0
        email_len = 0
        password_len = 0
        expected_output = True
        actual_output = len_bool_helper(user_name_len, email_len, password_len)
        self.assertEqual(expected_output, actual_output)

    def test_login_helper(self):
        """Test email is not equal to empty string"""
        email = ""
        expected_output = True
        actual_output = login_helper(email)
        self.assertEqual(expected_output, actual_output)

    def test_get_spotify_img(self):
        """Mock spotify img call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "images": [{"url": "www.com"}, {"url": "www.img.com"}]
        }

        with patch("spotify.requests.get") as mock_get:
            mock_get.return_value = mock_response
            result = spotify_api_image("1111", "1234")
            self.assertEqual(result, "www.img.com")

    def test_spotify_access_token_call(self):
        """Mock spotify access token call"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "1234"}
        with patch("spotify.requests.post") as mock_get:
            mock_get.return_value = mock_response
            result = spotify_access_token_call()
            self.assertEqual(result, "1234")


if __name__ == "__main__":
    unittest.main()
