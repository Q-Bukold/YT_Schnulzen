import os
import googleapiclient
from googleapiclient.discovery import build
import pandas as pd
import time

def tidy_and_save(list, filename):
    #convert to df
    data_df = pd.DataFrame(list, columns=['author', 'comment'])

    #delete newlines in comments
    data_df['comment'] = data_df['comment'].replace(r'\s+|\\n', ' ', regex=True) 
    #strip excess white spaces
    data_df['comment'] = data_df['comment'].str.strip()

    data_df.to_csv(filename, sep="\t")
    
    return data_df


def tsv_from_video(DEVELOPER_KEY, video_id, output_filename, order, max_lenght_output, sleep):

    #api
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube_api = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    is_first_page = True

    #prepare while-loop
    data = []
    next_page_token = ''

    while is_first_page or next_page_token and len(df) < max_lenght_output:
        is_first_page = False
        time.sleep(sleep)
        
        #get page
        page = youtube_api.commentThreads().list( #max 1 request per second
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
            item_list = []
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textOriginal"]
            #print("Comment by {}: {}".format(author, text))
            item_list.append(author)
            item_list.append(text)
            page_list.append(item_list)

        
        #get next page and repeat
        next_page_token = page["nextPageToken"]
        
        #save, in case of Error or API-Interrupt
        data += page_list
        df = tidy_and_save(data, output_filename)
        print(len(df))

    
    #final save
    df = tidy_and_save(data, output_filename)
    print("final len:", len(df))
    
    return df