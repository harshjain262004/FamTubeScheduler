import os
import googleapiclient.discovery 
from datetime import datetime, timedelta,timezone
from dotenv import load_dotenv
load_dotenv()
from Db import getQueries, AddVideos

# This function runs every minute to 
# fetch the latest videos from the Youtube API
# and add them to the database.
# It also updates the keyIndex to use a different API key
# every time the function runs.
# The keyIndex is stored in a file called keyIndex.txt 
def YoutubeAPIScript():
    start = str(datetime.now())
    print("Script Started: " + start)
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
    # Using Cicular counting to update the keyIndex 0...14...0...14
    updateKeyIndex((keyIndex+1)%15)
    end = str(datetime.now())
    print("Script Ended: " + end)
    print("Time taken: " + str(datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f") - datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")))
    print("Script Completion")
    return "Script Completion"

# This function is used to get the keyIndex from the file keyIndex.txt otherwisr return 0
def getIndexFromFile():
    with open("keyIndex.txt","r") as f:
        content = f.read()
        if content == "":
            return 0
        return int(content)

# This function is used to update the keyIndex in the file keyIndex.txt clear all content and write the new keyIndex
def updateKeyIndex(keyIndex):
    with open("keyIndex.txt","w") as f:
        f.write(str(keyIndex))
    return
