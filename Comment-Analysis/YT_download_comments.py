import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd
import time

#main
def list_from_video(DEVELOPER_KEY, video_id, order, max_lenght_output):
    is_first_page = True
    data = []
    next_page_token = ''
    youtube_api = init_api(DEVELOPER_KEY)
    sleep = 3 #increase, if download-limit is reached to fast
  
    while is_first_page or next_page_token and len(data) < max_lenght_output-5:
        page_list, is_first_page, page = get_page_data(is_first_page, next_page_token, sleep, youtube_api, video_id, order)
        data += page_list
        
        #get next page and repeat
        next_page_token = page["nextPageToken"]
        
        print(f"Status = {len(data)}/{max_lenght_output}")

    return data, len(data)



def init_api(DEVELOPER_KEY):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube_api = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    return youtube_api

def get_page_data(is_first_page, next_page_token, sleep, youtube_api, video_id, order):
    is_first_page = False
    time.sleep(sleep)
    
    #get page
    page = youtube_api.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id,
        textFormat="plainText",
        #is there a netxt page? If yes, get token:
        pageToken=next_page_token,
        order= order    #<- "time" or "relevance" (not the same as TOP-Comments on YT, but similar)
    ).execute()

    #get data from page into list
    page_list = []
    for item in page["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textOriginal"]
        #print("Comment by {}: {}".format(author, text))
        item = (author, text)
        page_list.append(item)
    
    return page_list, is_first_page, page