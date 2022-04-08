"""Spotify API python file"""
import os
import base64
import requests
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())  # This is to load your client id and client secret from .env


def spotify_access_token_call():
    """Spotify access token call"""
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

    return token_response_data["access_token"]


def spotify_api_image(artist_id, access_token):
    """This function retrieves image url from spotify"""

    headers = {"Authorization": f"Bearer {access_token}"}
    artist_img_endpoint = "https://api.spotify.com/v1/artists/"

    res = requests.get(artist_img_endpoint + artist_id, headers=headers)
    res_json = res.json()

    return res_json["images"][1]["url"]


def spotify_api():
    """Spotify API call function"""

    access_token = spotify_access_token_call()

    headers = {"Authorization": f"Bearer {access_token}"}

    endpoint = "https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M"

    resp = requests.get(endpoint, headers=headers)

    art = resp.json()
    names_list = []
    img_list = []
    for i in range(50):
        artist = art["tracks"]["items"][i]["track"]["artists"][0]["name"]
        artist_id = art["tracks"]["items"][i]["track"]["artists"][0]["id"]

        img_url = spotify_api_image(artist_id, access_token)

        if img_url not in img_list and artist not in names_list:
            img_list.append(img_url)
            names_list.append(artist)

    return names_list, img_list
