import unittest
from unittest.mock import MagicMock, patch
from spotify import spotify_api
from app import get_artists
import app
import json


class codeTests(unittest.TestCase):
    def test_spotify_api_call(self):
        bad_api_return_len = 30
        names_list, img_list = spotify_api()
        real_api_return_len = len(names_list)
        self.assertGreater(real_api_return_len, bad_api_return_len)


if __name__ == "__main__":
    unittest.main()
