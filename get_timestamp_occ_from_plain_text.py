import os
import re
import random
import datetime
import googleapiclient
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from googleapiclient.discovery import build
import pandas as pd

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "AIzaSyAYvRpVKJUS5MUnw6NVcIQB484ao6CdutE"
video_id = "hEMm7gxBYSc"
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)
list_all_comments = []
authors = []

def load_comments(match):
    for item in match["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textOriginal"]
        list_all_comments.append(text)
        authors.append(author)

        print("Comment by {}: {}".format(author, text))
        if 'replies' in item.keys():
            for reply in item['replies']['comments']:
                rauthor = reply['snippet']['authorDisplayName']
                rtext = reply["snippet"]["textOriginal"]
            print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")


def get_comment_threads(youtube, video_id, nextPageToken):
    results = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        videoId=video_id,
        textFormat="plainText",
        pageToken=nextPageToken
    ).execute()
    return results


match = get_comment_threads(youtube, video_id, '')
next_page_token = match["nextPageToken"]
load_comments(match)

try:
    while next_page_token:
        match = get_comment_threads(youtube, video_id, next_page_token)
        next_page_token = match["nextPageToken"]
        load_comments(match)
except:
    data = pd.DataFrame(list_all_comments, index=authors, columns=["Comments"])
    print(data)


def randomTime():
    # für 10 Minuten Videos
    # (4*60) = 240
    rtime = int(random.random() * 300)
    minutes = int(rtime / 60)
    seconds = rtime - minutes * 60
    time_string = '%02d:%02d' % (minutes, seconds)
    return time_string


def get_time(list_of_comments):
    list_of_times = []
    for text in list_of_comments:
        x = re.search(r"(?:([0-5]?[0-9]):)?([0-5]?[0-9]):([0-5][0-9])", text)
        if x is not None:
            str_with_time = x.group()
            list_of_times.append(str_with_time)
        else:
            pass
    return list_of_times


def delete_seconds(stamp):
    time_without_sec = []
    for x in stamp:
        x = x.split(":")
        x = x[0]
        time_without_sec.append(int(x))
    return time_without_sec


def stamp_to_second(stamp):
    list_sec_in_vid = []
    for x in stamp:
        x = x.split(":")
        minuten = int(x[0]) * 60
        sekunden = int(x[1])
        sec_in_vid = minuten + sekunden
        list_sec_in_vid.append(str(sec_in_vid))
    return list_sec_in_vid


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)



def round_stamps_10(stamps):
    out = []
    for txt in stamps:
        split_list = txt.split(":")
        if len(split_list) == 2:
            minutes, seconds = split_list
            seconds = int(seconds) / 10
            seconds = round(seconds)
            seconds = seconds * 10
            if seconds == 60:
                seconds = "00"
                minutes = int(minutes) + 1
            elif seconds == 0:
                seconds = '00'
            tpl = (str(minutes), str(seconds))
            rounded = ':'.join(tpl)
            out.append(rounded)
        else:
            pass
    return out




# print(list_all_comments)


extracted_time_stamps = get_time(list_all_comments)
print(extracted_time_stamps)

round_stamps_10_list = round_stamps_10(extracted_time_stamps)

as_times = []
for stamp in round_stamps_10_list:
    time = datetime.datetime.strptime(stamp, r'%M:%S')
    # print(time)
    as_times.append(time)
print(as_times)
as_times = sorted(as_times)
print(as_times)

# find all x-values
set_x = set(as_times)  # CHANGE
x_individual = list(set_x)
print(x_individual)

# count occuraces for y-axis
occ_x = []
for x in set_x:
    count = as_times.count(x)  # CHANGE
    occ_x.append(count)

# sort
x_individual = np.array(x_individual)

# PLOT
x_values = np.sort(x_individual)
y_values = np.array(occ_x)

fig, ax = plt.subplots()
ax.plot(x_values, y_values, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=12)
fig.set_figwidth(10)
fig.set_figheight(4)
ax.set_title("Number of Time Stamps per 10-Seconds")
plt.xlabel('Time in Video')
plt.ylabel('Number of Time-Stamps')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
plt.grid()

plt.show()
