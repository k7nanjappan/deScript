#---------------------------------------------------------
# Import Libraries:

# Parse URL
import urllib.parse as p

# Miscellaneous operating system interfaces
import os

# Read command line arguments
import sys

# Python object serialization
import pickle

# YouTube API v3 libraries 
# Source: https://developers.google.com/youtube/v3
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google PaLM API Library
# Source: https://makersuite.google.com/
import google.generativeai as palm

#---------------------------------------------------------
# YouTube Category ID Dictionary:

youtube_id = {
    "2": "Autos & Vehicles",
    "1": "Film & Animation",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers"
}

#---------------------------------------------------------
# Function Definitions:

# Authenticate YouTube API credentials
def authenticate_youtube_api():
    
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    client_secret_file = "keys/google_cloud_api_key.json"
    credentials = None

    if os.path.exists("keys/token.pickle"):
        with open("keys/token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:

        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            credentials = flow.run_local_server(port=0)

        # save the credentials for the next run
        with open("keys/token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build(api_service_name, api_version, credentials=credentials)


# Extract video_id from the URL format: https://www.youtube.com/watch?v=video_id
def extract_video_id(url):

    parsed_url = p.urlparse(url)

    video_id = p.parse_qs(parsed_url.query).get("v")

    if video_id:
        return video_id[0]
    
    else:
        raise Exception(f"Wasn't able to parse video URL: {url}")
    

# Retrive video info using YouTube API
def getVideoInfo(youtube_api, **kwargs):
    return youtube_api.videos().list(
        part = "snippet, contentDetails, statistics",
        **kwargs
    ).execute()

# Extract YouTube video title and channel name from URL
def extract_title_and_channel_title(youtube_link):

    video_id = extract_video_id(youtube_link)
    
    videoInfo = getVideoInfo(youtube_api, id = video_id)

    snippet = videoInfo.get("items")[0]["snippet"]

    return snippet["title"], snippet["channelTitle"], snippet["categoryId"]

# Initiates PaLM API for passing Bard prompts
def initiate_palm():

    palm_api_key_file = open("keys/palm_api_key.txt", "r")

    palm_api_key = palm_api_key_file.read()

    palm.configure(api_key = palm_api_key)

    models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]

    return models[0].name

# Send prompt to Bard and retrieve the response
def palm_request(prompt):
    
    model = initiate_palm()

    response = palm.generate_text(
        model = model,
        prompt = prompt,
        temperature=0,
        max_output_tokens = 1000,
    )

    return response.result

# Creates the appropriate Bard prompt based on the video category
def create_prompt(title, channel_title, category):
    
    if category == "Music":

        prompt = str(
        "Please provide a music video description by " +
        channel_title + 
        " by explaining the lyrics for the following YouTube video by " + 
        channel_title +
        " whose title is " +
        title)

    else:

        prompt = str(
            "Please provide a compelling third person video description as " +
            channel_title + 
            " in simple past tense for the following " +
            category +
            " YouTube video by " + 
            channel_title +
            " whose title is " +
            title)
    
    return prompt


#---------------------------------------------------------
# Authenticate YouTube API v3:

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

youtube_api = authenticate_youtube_api()

#---------------------------------------------------------
# Extract Video details:

# Obtain the YouTube Video URL passed as command line argument
youtube_link = sys.argv[1]

title, channel_title, category_id = extract_title_and_channel_title(youtube_link)

# Obtain category from the Category ID
category = youtube_id[category_id]

#---------------------------------------------------------
# Generate Description:

prompt = create_prompt(title, channel_title, category)

response = palm_request(prompt)

print(response)



