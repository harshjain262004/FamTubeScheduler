# **Fam Pay Youtube API Scheduler**

## API Reference

#### Get Videos in reverse chronological order 

```http
  GET /api/getVideos?page=<PAGE>&limit=<limit>&sort=<asc/desc>
```

| Parameter | Type     | Description                |Need|
| :-------- | :------- | :------------------------- |:-----|
| `page` | `int` | Default = 1 |Pagination|   
| `limit` | `int` | Default = 10 |Pagination|
| `sort` | `string` | Default = desc / Acceptable = asc|Requirement|


#### Get TotalVideosScraped

```http
  GET /api/getTotalVideo --> returns Total number of videos in Db
```

## How to run
### Setup Backend
    git clone https://github.com/harshjain262004/FamTubeScheduler.git

    cd backend

    *optional* create venv or virtual env and activate

    python -m pip install -r requirments.txt

    python app.py

    http://127.0.0.1:5000/api/getVideos?page=<PAGE>&limit=<limit>&sort=<asc/desc>
    example --> http://127.0.0.1:5000/api/getVideos?page=2&limit=10 

### Setup Frontend (Optional)
    cd frontend

    npm install or yarn install or pnpm install

    npm/yarn/pnpm run dev

## BONUS FEATURES
1. A simple next js app with features like debouncing and stats like total Videos available.
   ![image](https://github.com/user-attachments/assets/52afea40-9493-4a62-b4cc-d31609b4c2a2)

3. Multi API key support
### Algorithm used in circular switching (Multikey Support)
        We are running the scripts every 1 min, essentially 60*24 = 1440 times in 24 hours.
        The Google API key has a daily quota of 10000 units.
        1 Search request takes 100 units.
        Therefore the API key can only make 100 requests per day.
        As per this information a set of 15 keys is requried to run ~ 1500 times a day. 
        In .env file we have 15 keys named as YOUTUBE_API_KEY_{i} where i is 0 --> 14.
        Initialized with 0th key. 
        After the 1st job is done, in the file KeyIndex.txt the Index 1 is stores immediately.
        Next Job will take the 1st key, saving 2 in the file, and so on.
        0-1-2-3-4-5-6-7-8-9-10-11-12-13-14 -> 0-1....
        It is a circular approach to avoid exhaustion of keys.
    
    

    
## Methodolgy and Implementation
1. Built a Flask based backend application that runs a Youtube API asynchronously in the backend after a regular interval. (currently 1 minute).
--> Using APscheduler to Schedule timed jobs during the server runtime.

2. Calls Youtube API to return the youtube videos uploaded/publishedAfter a time period which is (5 Minutes prior to current time).
**PS:** Tried "1 to n" seconds prior to current time, but number of videos returned were pretty less, and chances to loose data since we are running the script every 1 min.

3. Gets the Videos_Json format and adds relevant details about the video to the database including video meta data, thumbnails, search query that gave the video as result, etc. 

4. Database in use is postgresql on the cloud hosted using neon free tier. There are two tables namely queries to store all the search queries that need to run in the job, and videos to store meta data about recieved results. 
-->Foreign key relation in Videos pointing to what query was used.

5. Both the tables have primary keys and essentially a index.
   
-->queries (id) int auto increment. (PK)

-->Videos (Video_Id) Unique String from youtube. (PK)

-->Index ON videos (published_at DESC) (Faster sort based lookups on timestamp at which youtube video was published)

6. Actual Requirements
--> To build a API endpoint to fetch videos data in **chronologically reversed**. More importantly made it modular to run asc, desc commands from single api along with **pagination, offset**.
More in API refference.

