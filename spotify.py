"""Spotify API python file"""
# pylint: disable=invalid-name
# pylint: disable=too-many-locals
import os
import base64
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())  # This is to load your client id and client secret from .env


def spotify_api():
    """Spotify API call function"""
    client_id = os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    client_creds = f"{client_id}:{client_secret}"
    client_creds_b64 = base64.b64encode(client_creds.encode())
    token_url = "https://accounts.spotify.com/api/token"

    token_data = {
        "grant_type": "client_credentials",
    }

    token_headers = {"Authorization": f"Basic {client_creds_b64.decode()}"}

    req = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = req.json()

    access_token = token_response_data["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    endpoint = "https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M"
    artist_img_endpoint = "https://api.spotify.com/v1/artists/"

    resp = requests.get(endpoint, headers=headers)

    a = resp.json()
    names_list = []
    img_list = []
    for i in range(50):
        artist = a["tracks"]["items"][i]["track"]["artists"][0]["name"]
        artist_id = a["tracks"]["items"][i]["track"]["artists"][0]["id"]
        res = requests.get(artist_img_endpoint + artist_id, headers=headers)
        res_json = res.json()

        img_url = res_json["images"][1]["url"]
        if img_url not in img_list and artist not in names_list:
            img_list.append(img_url)
            names_list.append(artist)

    return names_list, img_list
