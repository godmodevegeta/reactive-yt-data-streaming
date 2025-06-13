#!/usr/bin/env python3

import logging
import sys
import requests
from config import config

def fetch_playlist_page(api_key, playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", 
                            params={
                                "key": api_key,
                                "playlistId": playlist_id,
                                "part": "contentDetails",
                                "pageToken": page_token    
                            })
    return response.json()
    


# def fetch_playlist_info(api_key, playlist_id, page_token=None):
#     fetch_playlist_page(api_key, playlist_id, page_token)
#     logging.debug(response.text)

def main():
    logging.info("Hello, there!")
    api_key = config["google_api_key"]
    playlist_id = config["playlist_id"]
    logging.info("found key: %s", api_key)
    fetch_playlist_page(api_key, playlist_id, "EAAaHlBUOkNBVWlFREl4UkRKQk5ETXlORU0zTXpKQk16SQ")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())