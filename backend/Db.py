import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2

POSTGRES_URL = os.environ["POSTGRES_API"] 
connection = psycopg2.connect(POSTGRES_URL)
cursor = connection.cursor()

def getQueries():
    cursor.execute("SELECT query,id FROM queries")
    queries = cursor.fetchall()
    return queries

def AddVideos(response,query):
    id = getId(query)
    pass
    # figure out what to store, and indexing for good performance fetch queries

def getId(query):
    cursor.execute("SELECT id FROM queries WHERE query = %s", (query,))
    id = cursor.fetchone()
    return id[0]