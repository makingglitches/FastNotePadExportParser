
import sqlite3
import pathlib
import os
import io
import fastnoteTool
import sqlitestoremgr
import fixposunicodecrap as uni
import hashlib

print(sqlitestoremgr.dir)

keydict = {}

inputfilename = "input/FastNotepad_2024-04-23"

empty_db_path = "fastnoteparser/notedatabase_empty.sqlite"
output_db_path = "output/notedatabase.sqlite"

sqlmgr = sqlitestoremgr.sqlitestoremanager(empty_db_path,output_db_path)


#check = sqlmgr.Get_Contents('bmrmd38t508h59fo')

def HandleIRecord(recnum,rec):

    global keydict
    print(rec)

    update = sqlmgr.AddOrUpdateIndex(rec[0],
                            float(rec[3]),
                            int(rec[6]),
                            rec[9],
                            rec[1],
                            True if rec[7] == '1' else False,
                            True if rec[4] == 'i2' else False,
                            False)
    
    keydict[rec[0]] = (update,int(rec[6]), rec[4])

def HandleCRecord(recnum,rec):
    
    global keydict
    print(rec)


    # should ALWAYS be the case.
    if rec[0] in keydict:
        savedkey = keydict[rec[0]]

        # unescaped_contents = bytes(rec[1],'utf-8').decode('unicode_escape')
        # fuck. fastnotepad stores emojois and only 
        # counts the fucking characters once.
        # there is a big problem with it miscounting 
        # unicode characters
        # so. once again here comes the suck.
        # this whole stupid thing breaks down right here.
        # i have to kind of guess, which means I also have to cheat.
        # it seems to be within like 1 or 2 either way.
        # seemed like they were counting each single character
        # as 2 bytes.
        # get the count of unicode characters in the string 
        finalstring = rec[1].encode('raw_unicode_escape').decode('unicode_escape')

        chars = uni.countUnicodeChars(finalstring)

        if (chars['countunicodechar'] > 0):
            #print ("this will be obsolete via the next update")
            #print ("or soon there after its whats causing the")
            #print ("the import bug. or was.")

            print (f'file says:{savedkey[1]}')
            print (f'program is finding:')
            print (chars)

            # here comes the cheating suck.
            indexbinder = sqlmgr.GetIndex(rec[0])

            if (indexbinder[0].EpochTime == savedkey[0] 
                and indexbinder[0].NoteLength==savedkey[1]):
                sql = "UPDATE NOTEINDEXES SET NOTELENGTH=? WHERE KEY=?"
                db = sqlmgr.OpenDb()
                db.execute(sql,(len(finalstring), rec[0]))
                db.commit()
            else:
                for p in indexbinder[1]:
                    if (p.UpdateTime == savedkey[0] and 
                        p.NoteLength == savedkey[1]):
                        sql = "UPDATE NOTEINDEXES_UPDATES set NOTELENGTH=? where updatekey = ?"
                        db = sqlmgr.OpenDb()
                        db.execute(sql,(len(finalstring),p.UpdateKey))
                        db.commit()

        keydict[rec[0]] = (savedkey[0], len(finalstring))
        savedkey = keydict[rec[0]]

        if len(finalstring) != savedkey[1]:
            raise f"malformed content record, aborting. error at key {rec[0]}"

        sqlmgr.AddOrUpdateContents(rec[0],
                                   finalstring,
                                   rec[2], 
                                   savedkey[0])


# run the import 
fnt = fastnoteTool.fastNoteTool(filename=inputfilename,_verbose=True)
fnt.OnCRecord = HandleCRecord
fnt.OnIRecord = HandleIRecord

fnt.run()

# consolidate to final records.







