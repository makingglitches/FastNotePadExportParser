
import sqlite3
import pathlib
import os
import io
import fastnoteTool
import sqlitestoremgr

import hashlib
import datetime

print(sqlitestoremgr.dir)

# set this to 1 to see file contents during processing
VERBOSE=0

##### Place all files to be processed in the project_dir/input/FastNotePad

empty_db_path = "fastnoteparser/notedatabase_empty.sqlite"
output_db_path = "output/notedatabase.sqlite"

sqlmgr = sqlitestoremgr.sqlitestoremanager(empty_db_path,output_db_path)
keydict = {}


#check = sqlmgr.Get_Contents('bmrmd38t508h59fo')

def HandleIRecord(recnum,rec,sha):

    global keydict
    global VERBOSE

    if VERBOSE==1:
        print(rec)

    update = sqlmgr.AddOrUpdateIndex(
                                    _key=rec['key'],
                                    _epochtime=rec['epochtime'],
                                    _notelength = rec['notelength'],
                                    _preview = rec['preview'],                                    
                                    _folder = rec['folder'],
                                    _starred = rec['starred'],
                                    _complete = rec['complete'],
                                    _reviewed = False,
                                    _filesrckey = sha)
    
    keydict[rec['key']] = update

def HandleCRecord(recnum,rec,sha):
    
    global keydict
    global VERBOSE

    if VERBOSE==1:
        print(rec)


    # should ALWAYS be the case.
    if rec['key'] in keydict:
        storedtime = keydict[rec['key']]

        sqlmgr.AddOrUpdateContents(_key=rec['key'],
                                   _contents = rec['contents'],
                                   _scrollinfo= rec['scrolly'], 
                                   _filesrckey = sha,
                                   _updatetime=storedtime)


def runimport(ifilename,_sha):
    global keydict
    keydict = {}

    # run the import 
    fnt = fastnoteTool.fastNoteTool(filename=ifilename,_verbose=False, sha=_sha)
    fnt.OnCRecord = HandleCRecord
    fnt.OnIRecord = HandleIRecord

    fnt.run()

if __name__== "__main__":

    inputfiles = []

    fastnotepath = pathlib.Path('input/FastNotePad')

    for i in os.walk(fastnotepath):
        for f in i[2]:
            inputfiles.append(f)

    inputfiles.sort()

    for f in inputfiles:
        
        res = sqlmgr.FileProcessed( fastnotepath.joinpath(f))
        sha = res[2]

        if (res[0]==1):
            print(f"File: {f} with Sha256Sum: {sha} already processed")
        else:
            # when the import breaks this is the most likely starting point.
            sqlmgr.InsertFile(f ,sha,datetime.datetime.now())
            print(f"Processing {f}")

            runimport(fastnotepath.joinpath(f),sha)

    # need to add consolidate to final records script call.







