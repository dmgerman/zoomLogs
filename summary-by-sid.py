#!/usr/bin/python3


import fileinput
import itertools

allRecords = fileinput.input()

def toDict(x):
    return dict(zip(["cid","date","sid","min","from","to","n"], x.rstrip().split(',')))

records =  filter(lambda x: x['sid'] != 'sid', map(toDict, allRecords))

rSorted = sorted(list(records), key=lambda x: x['sid'])

grouped = [list(g) for k, g in itertools.groupby(rSorted, lambda x: x['sid'])]

def processStudent(stRec):
    assert(len(stRec)>=1)
    sid = stRec[0]["sid"]
    onlyDateMinPairs = sorted(map(lambda x: (x['date'], x['min']), stRec))
    return (sid,dict(onlyDateMinPairs))

perStudent = map(processStudent, grouped)

attDict = dict(perStudent)

me = attDict['V00000000']

for st in attDict:
    print(st, end="")
    for k in me.keys():
        try:
            theTime = attDict[st][k]
        except KeyError:
            theTime = ""
        print("",k,theTime,me[k],sep=",", end="")
    print("")


