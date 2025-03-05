import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
import json

# Using psycopg2 as a database driver to connect to the Postgres database at neon tech free Tier
POSTGRES_URL = os.environ["POSTGRES_API"] 
connection = psycopg2.connect(POSTGRES_URL)
cursor = connection.cursor()

# This Function is used to get the queries from the database
def getQueries():
    cursor.execute("SELECT id,query FROM queries")
    queries = cursor.fetchall()
    return queries

# This Function is used to add the videos to the database
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
        cursor.execute("INSERT INTO videos (video_id,title,description,published_at,channel_id,channel_title,thumbnails,query_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (video_id) DO NOTHING",(videoId,title,description,publishedAt,channelId,channelTitle,thumbnailsJson,query_id))
        connection.commit()
    return "Videos added to the database"

# This function is used to fetch the videos from the database in descending order of their published date (Pagination and Offset)
def fetchVideos(page, limit):
    offset = (page - 1) * limit
    query = """
        SELECT * FROM queries INNER JOIN videos ON videos.query_id = queries.id 
        ORDER BY published_at DESC 
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()
    return [
        {  
            "query": row[1],
            "video_id": row[2],
            "title": row[3],
            "description": row[4],
            "published_at": row[5],
            "channel_id": row[6],
            "channel_title": row[7],
            "thumbnails": row[8],
        }
        for row in rows
    ]

# This function is used to fetch the videos from the database in ascending order of their published date
def fetchVideosAsc(page, limit):
    offset = (page - 1) * limit
    query = """
        SELECT * FROM queries INNER JOIN videos ON videos.query_id = queries.id 
        ORDER BY published_at ASC 
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (limit, offset))
    rows = cursor.fetchall()
    return [
        {  
            "query": row[1],
            "video_id": row[2],
            "title": row[3],
            "description": row[4],
            "published_at": row[5],
            "channel_id": row[6],
            "channel_title": row[7],
            "thumbnails": row[8],
        }
        for row in rows
    ]

# This function is used to get the total number of videos in the database
def getTotalVideos():
    cursor.execute("SELECT COUNT(*) FROM videos")
    total = cursor.fetchone()[0]
    return total

# This function is used to fetch the videos from the database based on the query like cricket (Pagination and offset)
# Currently only 1 query "cricket" is present in the database so not in use
def fetchVideosQuery(page, limit, query_str):
    offset = (page - 1) * limit
    query = """
        SELECT * FROM queries INNER JOIN videos ON videos.query_id = queries.id
        WHERE query = %s 
        ORDER BY published_at DESC 
        LIMIT %s OFFSET %s;
    """
    cursor.execute(query, (query_str, limit, offset))
    rows = cursor.fetchall()
    return [
        {  
            "query": row[1],
            "video_id": row[2],
            "title": row[3],
            "description": row[4],
            "published_at": row[5],
            "channel_id": row[6],
            "channel_title": row[7],
            "thumbnails": row[8],
        }
        for row in rows
    ]