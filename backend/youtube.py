import os
import googleapiclient.discovery 
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
load_dotenv()
from Db import getQueries, AddVideos

def YoutubeAPIScript():
    keyIndex = getIndexFromFile()
    api_service_name = "youtube"
    api_version='v3'
    developer_key = os.environ[f"YOUTUBE_API_KEY_{keyIndex}"]
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)
    queries = getQueries()
    if len(queries) == 0:
        print("No queries present in the database")
        return "No queries present in the database"
    for id,query in queries:
        published_after = (datetime.now(timezone.utc) - timedelta(minutes=5)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")
        request = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=50,
            type="video",
            publishedAfter=published_after,
            order="date"
        )
        response = request.execute()
        AddVideos(response,id)
    updateKeyIndex((keyIndex+1)%15)
    print("Script Completion")
    return "Script Completion"

def getIndexFromFile():
    with open("keyIndex.txt","r") as f:
        if f.read() == "":
            return 0
        keyIndex = int(f.read())
    return keyIndex

def updateKeyIndex(keyIndex):
    with open("keyIndex.txt","w") as f:
        f.write(str(keyIndex))
    return
