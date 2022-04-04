"""Python file of unit tests"""
# pylint: disable=unused-variable
import unittest
from spotify import spotify_api


class CodeTests(unittest.TestCase):
    """python testing class"""

    def test_spotify_api_call(self):
        """First python test"""
        bad_api_return_len = 30
        names_list, img_list = spotify_api()
        real_api_return_len = len(names_list)
        self.assertGreater(real_api_return_len, bad_api_return_len)


if __name__ == "__main__":
    unittest.main()
