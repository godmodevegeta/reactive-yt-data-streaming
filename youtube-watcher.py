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
    


def fetch_playlist_info(api_key, playlist_id, page_token=None):
    page = fetch_playlist_page(api_key, playlist_id, page_token)
    
    yield from page["items"]
    next_page_token = page.get("nextPageToken")
    logging.info("found nextagetoken: %s", next_page_token)
    if next_page_token:
        yield from fetch_playlist_info(api_key, playlist_id, next_page_token)



def main():
    logging.info("Hello, there!")
    api_key = config["google_api_key"]
    playlist_id = config["playlist_id"]
    logging.info("found key: %s", api_key)
    for video_item in fetch_playlist_info(api_key, playlist_id, ):
        logging.info(video_item)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())