import re
import random
import matplotlib.pyplot as plt
import numpy as np




def randomTime():
    # für 10 Minuten Videos
    # (10*60) = 600
    rtime = int(random.random() * 600)
    minutes = int(rtime / 60)
    seconds = rtime - minutes * 60
    time_string = '%02d:%02d' % (minutes, seconds)
    return time_string


def get_time(list_of_comments):
    list_of_times = []
    for text in list_of_comments:
        x = re.search("[0-5]?[0-9]\\:[0-9][0-9]", text)
        str_with_time = x.group()
        list_of_times.append(str_with_time)
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
        minuten = int(x[0])*60
        sekunden = int(x[1])
        sec_in_vid = minuten + sekunden
        list_sec_in_vid.append(sec_in_vid)
    return list_sec_in_vid


#create test-comments
list_all_comments = []
for i in range(50):
    comment_i = ("Mega Video :D Ich gebe den 2 eine 10/10, gerade bei Minute " + randomTime() + "!!!")
    list_all_comments.append(comment_i)
    if i <= 10:
        print(comment_i)

extracted_time_stamps = get_time(list_all_comments)
print(extracted_time_stamps)
extracted_only_minutes = delete_seconds(extracted_time_stamps)
print(extracted_only_minutes)

#create x and y values for plot

#find all x-values
set_x = set(extracted_only_minutes) #CHANGE
list_x = list(set_x)

#count occuraces for y-axis
list_y = []
for x in set_x:
    count = extracted_only_minutes.count(x) #CHANGE
    list_y.append(count)

print("x-Werte = ", list_x)
print("y-Werte = ", list_y)


#plot
plt.plot(list_x, list_y, color='green',
         #marker='o',
         linestyle='dashed', linewidth=2, markersize=12)
#plt.gcf().autofmt_xdate()
plt.xlabel('Minutes in Video')
plt.ylabel('Number of Time-Stamps')
plt.xticks(list_x)
plt.grid()
plt.show()


'''
var timePattern = /(([0-5][0-9])|[0-9])\:[0-9]{2,2}/;
var seconds = "";

for (var i = 0; i < comments.length; i++) {
    var matches = comments[i].match(timePattern);
    var matched = matches[0];
    var a = matched.split(':');
    if(matched.length == 7 || matched.length == 8) {
        seconds = (+a[0])*60*60 + (+a[1])*60 + a[2];        
    } else {
        seconds = (+a[0])*60 + (+a[1]); 
    }
    times.push(seconds);
} '''
