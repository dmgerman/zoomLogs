#!/usr/bin/python3


import fileinput
import itertools

allRecords = fileinput.input()

records =  filter(lambda x: x[0] != 'sid', map(lambda x: x.rstrip().split(','), allRecords))

rSorted = sorted(list(records), key=lambda x: x[2])

grouped = [list(g) for k, g in itertools.groupby(rSorted, lambda x: x[2])]

def processStudent(stRec):
    assert(len(stRec)>=1)
    sid = stRec[0][2]
    onlyDateMinPairs = sorted(map(lambda x: (x[1], x[3]), stRec))
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


