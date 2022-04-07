"""Python file of unit tests"""
import unittest

# from spotify import spotify_api, spotify_access_token_call
from app import len_bool_helper, get_artists_helper, TopArtists


class CodeTests(unittest.TestCase):
    """python testing class"""

    # def test_spotify_api_call(self):
    #     """Spotify API test"""
    #     bad_api_return_len = 30
    #     names_list, _ = spotify_api()
    #     real_api_return_len = len(names_list)
    #     self.assertGreater(real_api_return_len, bad_api_return_len)

    # def test_spotify_access_token_call(self):
    #     """Access token test"""
    #     bad_access_token_len = 0
    #     real_access_token_len = len(spotify_access_token_call())
    #     self.assertGreater(real_access_token_len, bad_access_token_len)

    def test_len_bool_helper(self):
        """Length of fields in signup helper test"""
        user_name_len = 0
        email_len = 0
        password_len = 0
        expected_output = True
        actual_output = len_bool_helper(user_name_len, email_len, password_len)
        self.assertEqual(expected_output, actual_output)

    def test_get_artists_helper(self):
        """Test get artists helper function"""
        artist_entry = [
            TopArtists(
                id=1,
                ranking=1,
                artist_name="hayes",
                artist_image="png",
            )
        ]
        expected_output = [
            {"id": 1, "artist_name": "hayes", "artist_img": "png", "artist_rank": 1}
        ]
        actual_output = get_artists_helper(artist_entry)
        self.assertEqual(expected_output, actual_output)

    # @mock.patch("spotify.requests", return_value=([]))
    # def mock_test_api(self):
    #     """Mock test"""
    #     actual_result = spotify_api()

    #     expected_result = []
    #     self.assertEqual(actual_result, expected_result)


if __name__ == "__main__":
    unittest.main()
