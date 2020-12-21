#!/usr/bin/python3

import fileinput
import itertools
import datetime
import operator
import csv
import sys
import dateparser
import functools
    
from operator import itemgetter

#min = "10/26/2020 04:30:00 PM"
#min = "10/26/2020 01:00:00 PM"
#max = "10/26/2020 05:50:00 PM"
#max = "10/26/2020 06:00:00 PM"
#max = "10/26/2020 02:30:00 PM"

minTime = sys.argv.pop(1)
lectureLength = sys.argv.pop(1)

import itertools

def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b) 


timeFormat = '%m/%d/%Y %I:%M:%S %p'

def convert_zoom_time(st):
    # convert only the time
    return datetime.datetime.strptime(st, timeFormat)

def extract_date(str):
    d = convert_zoom_time(str)
    return(d.strftime("%Y-%m-%d"))

minObj = None
maxObj = None



def convert_to_abs(timeStr):
    # returns a number of minutes from starting of meeting
    timeObj = convert_zoom_time(timeStr)
    if timeObj < minObj:
        return 0
    if timeObj > maxObj:
        return (maxObj - minObj).seconds
    else:
        return (timeObj - minObj).seconds

def time_from(l):
    return convert_to_abs(l[1])

def time_to(l):
    return convert_to_abs(l[2])
    
def convert_to_time_present(recordList):
    timesP = sorted(map(lambda x: (time_from(x), time_to(x)), recordList))
    return timesP;


def merge_times(listRecords):
    if len(listRecords) <= 1:
        return listRecords
    else:
        (f1,t1) = listRecords[0]
        (f2,t2) = listRecords[1]
        assert f1 <= f2, "list should be sorted"
        if (t1 >= f2): # merge first, recourse on entire list
            return merge_times([(f1,t2)] + listRecords[2:])
        else: # skip first, merge the rest
            return [listRecords[0]] + merge_times(listRecords[1:])

def verify_merged(list):
    for ((f1,t1),(f2,t2)) in pairwise(list):
        assert(f1 <= t1)
        assert(f2 <= t2)
        assert(t1 < f2)
    

def sum_times(l):
    seconds = map(lambda p:  p[1]-p[0], l )
    total = functools.reduce(lambda x,acc: x + acc, seconds, 0)
    return total

def convert_to_minutes(recordList):
    times = convert_to_time_present(recordList)
    merged = merge_times(times)
    verify_merged(merged)
    seconds = sum_times(merged)
    min = seconds*1.0/60
    return min

def get_course_id_and_date(header):
    # at the same time assert the times
    fields = header.rstrip().split(',')
    timeFrom = convert_zoom_time(fields[2])
    timeTo = convert_zoom_time(fields[3])
    return (fields[1], extract_date(fields[2]))
    



# process the data


allRecords = fileinput.input()

# process the header (first 4 lines)
header = next(allRecords)
meetingInfo = next(allRecords)
# verify the headers
assert next(allRecords).rstrip() == "" # empty line
assert next(allRecords).rstrip() == "sid,Leave Time,Duration (Minutes)"


(courseId,dateLecture) = get_course_id_and_date(meetingInfo)

def get_full_time(date, timeStart, timeMinutes):
    tFormat = '%Y-%m-%d %I:%M:%S %p'
    startTime = datetime.datetime.strptime(date + " " + minTime, tFormat)
    delta = datetime.timedelta(minutes=int(timeMinutes))
    endTime = startTime + delta
    return (startTime, endTime)
    

(minObj, maxObj) = get_full_time(dateLecture, minTime, lectureLength) # set the start time and end time


records =  filter(lambda x: x[0] != 'NOLONGER', map(lambda x: x.rstrip().split(','), allRecords))


rSorted = sorted(list(records), key=lambda x: x[0])
#print (rSorted)

grouped = [list(g) for k, g in itertools.groupby(rSorted, lambda x: x[0])]

#print(list(grouped)[0])

print ("sid;lectureTimeAttended;firstTime;lastTime")

for studentRecords in grouped:
    minutes = "{:.1f}".format(convert_to_minutes(studentRecords))
    first = studentRecords[0]
    last = studentRecords[-1]
    sid = first[0] # there is at least one
    timeFrom = studentRecords[0][1] # there is at least one
    print(courseId, dateLecture, sid, minutes, first[1], last[2], len(studentRecords), sep=",")
        
 


exit(0)

l = [
     ["Immanuel","imma@uvic.ca","10/26/2020 04:25:35 PM","10/26/2020 05:55:54 PM","91"],
     ["Daniel German","dmg@uvic.ca","10/26/2020 04:25:07 PM","10/26/2020 05:59:29 PM","95"],
    ["Joshua","dasfd@uvic.ca","10/26/2020 04:25:37 PM","10/26/2020 05:56:18 PM","91"]

    ]

l2 = [
     ["Immanuel","im@uvic.ca","10/26/2020 04:25:35 PM","10/26/2020 04:55:54 PM","91"],
     ["Daniel German","dmgx@uvic.ca","10/26/2020 05:25:07 PM","10/26/2020 05:59:29 PM","95"],
     ["Joshua","j@uvic.ca","10/26/2020 04:59:37 PM","10/26/2020 05:56:18 PM","91"]
    ]


convert_to_times_sequence(l2)
exit(0)
                
