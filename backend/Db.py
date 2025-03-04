import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
import json

POSTGRES_URL = os.environ["POSTGRES_API"] 
connection = psycopg2.connect(POSTGRES_URL)
cursor = connection.cursor()

def getQueries():
    cursor.execute("SELECT id,query FROM queries")
    queries = cursor.fetchall()
    return queries

def AddVideos(response,query_id):
    videos = response["items"]
    for video in videos:
        videoId = video["id"]["videoId"]
        videoDetails = video["snippet"] 
        title = videoDetails["title"]
        description = videoDetails["description"]
        publishedAt = videoDetails["publishedAt"]
        channelId = videoDetails["channelId"]
        thumbnails = videoDetails["thumbnails"]
        thumbnailsJson = json.dumps(thumbnails)
        channelTitle = videoDetails["channelTitle"]
        cursor.execute("INSERT INTO videos (video_id,title,description,published_at,channel_id,channel_title,thumbnails,query_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",(videoId,title,description,publishedAt,channelId,channelTitle,thumbnailsJson,query_id))
        connection.commit()
    print("Videos added to the database: ", len(videos))
    return "Videos added to the database"
