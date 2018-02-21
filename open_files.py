import os
import re

from os import walk
from os import listdir
from os.path import isfile, join

procPath = '/proc'
passwdFile = '/etc/passwd'
userName = {}

def readUserNames():
    global userName
    try:
        with open(passwdFile) as search:
            for line in search:
                line = line.rstrip()
                attrs = line.split(":")
                userName[attrs[2]] = attrs[0]
    except:
        print "Unable to read passwd file!"
        raise

def readFileRegex( FNAME, rePattern ):
    keyPattern = re.compile(rePattern)
    try:
        with open(FNAME) as search:
            for line in search:
                line = line.rstrip()
                if keyPattern.match(line):
                    keyValue = keyPattern.match(line).group(1)
                    break
        return keyValue
    except:
        return None

def getUserIdByPid( PID ):
    procStatus = procPath + "/" + PID + "/status"
    uidPattern = re.compile("^Uid:\s\d+\s(\d+)\s\d+\s\d+")
    userId = readFileRegex( procStatus, uidPattern )
    return userId

def getMaxFilesForPid( PID ):
    procLimits = procPath + "/" + PID + "/limits"
    nofilesPattern = re.compile("^Max open files\s+\d+\s+(\d+)\s+files")
    maxFiles = readFileRegex(procLimits, nofilesPattern)
    return maxFiles

readUserNames()

pidFilesOpen = {}
pidOwner = {}
pidMax = {}
pidUtilization = {}

dirList = []
for (dirpath, dirnames, filenames) in walk(procPath):
    dirList.extend(dirnames)
    break

fileList = []
pidPattern = re.compile("^[0-9]*$")
for PID in dirList:
    if pidPattern.match(PID):
        try:
            fileList = os.listdir(procPath + "/" + PID + "/fd")
            userId = getUserIdByPid(PID)
            maxFiles = getMaxFilesForPid(PID)
            filesOpen = len(fileList)
            percentOpen = float(filesOpen) / float(maxFiles) 

            pidFilesOpen[PID]   = filesOpen
            pidOwner[PID]       = userId
            pidMax[PID]         = maxFiles
            pidUtilization[PID] = percentOpen
        except:
            pass

try:
    for key, value in sorted(pidUtilization.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        print pidUtilization[key], "pid:", key, " user:", userName[pidOwner[key]]
except:
    pass

