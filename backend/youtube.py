import os
import googleapiclient.discovery 
from datetime import datetime, timedelta,timezone
import pprint

api_service_name = "youtube"
api_version='v3'
developer_key = "AIzaSyB1i3S7W-eGrhiKJXecps94YoQZjoN_zZY"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)

def YoutubeAPIScript():
    published_after = (datetime.now(timezone.utc) - timedelta(minutes=5)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
    request = youtube.search().list(
        q="Cricket",
        part="id,snippet",
        maxResults=50,
        type="video",
        publishedAfter=published_after,
        order="date"
    )
    response = request.execute()
    return response
