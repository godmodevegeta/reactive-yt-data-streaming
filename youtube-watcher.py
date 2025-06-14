#!/usr/bin/env python3

import logging
import sys
import requests
from config import config
from pprint import pformat

def fetch_playlist_page(api_key, playlist_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/playlistItems", 
                            params={
                                "key": api_key,
                                "playlistId": playlist_id,
                                "part": "contentDetails",
                                "pageToken": page_token    
                            })
    return response.json()

def fetch_video_page(api_key, video_id, page_token=None):
    response = requests.get("https://www.googleapis.com/youtube/v3/videos", 
                            params={
                                "key": api_key,
                                "id": video_id,
                                "part": "snippet,statistics",
                                "pageToken": page_token    
                            })
    return response.json()
    


def fetch_playlist_info(api_key, playlist_id, page_token=None):
    page = fetch_playlist_page(api_key, playlist_id, page_token)
    
    yield from page["items"]
    next_page_token = page.get("nextPageToken")
    if next_page_token:
        yield from fetch_playlist_info(api_key, playlist_id, next_page_token)

def fetch_videos(api_key, video_id, page_token=None):
    page = fetch_video_page(api_key, video_id, page_token)
    
    yield from page["items"]
    next_page_token = page.get("nextPageToken")
    if next_page_token:
        yield from fetch_videos(api_key, video_id, next_page_token)
    
def summarize_video(video):
    return {
        "videoId": video.get("id"),
        "title": video.get("snippet").get("title"),
        "views": int(video.get("statistics").get("viewCount")),
        "likes": int(video.get("statistics").get("likeCount")),
        "comments": int(video.get("statistics").get("commentCount")),
    }

def main():
    logging.info("Hello, there!")
    api_key = config["google_api_key"]
    playlist_id = config["playlist_id"]
    logging.info("found key: %s", api_key)
    for video_item in fetch_playlist_info(api_key, playlist_id, ):
        video_id = video_item.get("contentDetails").get("videoId")
        for video in fetch_videos(api_key, video_id, ):
            logging.info(pformat(summarize_video(video)))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sys.exit(main())