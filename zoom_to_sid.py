#!/usr/bin/python3

import fileinput
import sys
import csv

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

sidsFile = sys.argv.pop(1)


with open(sidsFile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    sidsList = list(map(lambda x: (x[1],x[2]), csv_reader))
    sids = dict(list(sidsList) + [("dmg","V00000000")])

allRecords = fileinput.input()

for i in range(0,3):
    print(next(allRecords).rstrip())

header = "Name (Original Name),User Email,Join Time,Leave Time,Duration (Minutes)"
h = next(allRecords).rstrip()
#print(h[0:len(header)])
assert header[0:len(header)] == h[0:len(header)]
print ("sid,Leave Time,Duration (Minutes)")

records =  filter(lambda x: x[1] != '', map(lambda x: x.rstrip().split(','), allRecords))

lastField = 5
def transcode (r):
    student = r[1].split('@',1)[0]
    try:
        return [sids[student] ] + r[2:lastField]
    except KeyError:
        return ["NOLONGER"] + r[2:lastField]
     
    

printable = map(transcode, records)

for r in printable:
    print(','.join(r))

