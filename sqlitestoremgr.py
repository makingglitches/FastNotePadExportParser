import pathlib
import sqlite3
import uuid
import datetime
import hashlib
import json
import random
from collections import Counter

# byte values 

# 48 to 57  = 0 to 9
# 65 to 90  = A to Z
# 97 to 122 = a to z


# defines an array of all the ascii values for 0-9, A-Z, and a-z
bytevalues = list(range(48,57)) + list(range(65,90)) + list(range(97,122))

# default buffer size of 5 MB
buffersize = 1024*1024*5




# this is to generate new keys for indexes added by this program to retain
# consistency.
def generateAlphaNumeric(length = 16):
    i=0 
    s = ""

    while (i < length):
        c = int(random.random() * (len(bytevalues)-1))
        char = bytevalues[c].to_bytes(1).decode()
        s = s + char
        i = i + 1

    return s


# gets the directory where the sql files for this project are stored.
# should be in a subdirectory "sql_files" where the code file is stored.
dir = pathlib.Path(__file__).parent.joinpath("sql_files")

def filecopy(ipath:str,opath:str,callback = None):
    """
    Just copies a file from one location to another.

    Args:
        ipath (str): input file path
        opath (str): output file path
        callback (function, optional): callback function accepting one integer argument. Defaults to None.
    """    
    global buffersize
    inp = open(ipath,"rb")
    out = open(opath,"wb")

    b = inp.read(buffersize*5)

    while b:
        out.write(b)
        out.flush()

        if callback:
            callback(len(b))
        
        b = inp.read(buffersize*5)

    inp.close()
    out.flush()
    out.close()

def readallBytes(filename:str)->bytes:
    f = open(filename,'rb')
    b = f.read()
    f.close()
    return b

def readall(filename:str)->str:
    f = open(filename,"r")
    s =  f.read()
    f.close()
    return s

def ObjListToJson(l):
    js = '['

    for i in l:
        if isinstance(i,list):
            js = js + ObjListToJson(i) + ","
        else:
            js = js + json.dumps(i, default=lambda x: x.__dict__) +","

    js = js.rstrip(',') + ']'

    return js

def fieldexistssql(field,table):
    return f"select exists (select null from [{table}] where [{field}] =? )"


class Statistics:
    def __init__(self,_key, _killings,_saved,_drugged,_thefts, _informed) -> None:
        self.Key = _key
        self.Killings = _killings
        self.Saved= _saved
        self.Drugged = _drugged
        self.Thefts = _thefts
        self.Informed = _informed

    @staticmethod 
    def mapSql(rec):
        return Statistics(rec[0],rec[1],rec[2],rec[3],rec[4],rec[5])
    
    def InsertOrUpdate(self, s:"sqlitestoremanager"):
        s.AddOrUpdateStatistics(self.Key,
                                self.Killings,
                                self.Saved,
                                self.Drugged,
                                self.Thefts,
                                self.Informed)        
class NoteIndex:
    """
    Dataclass representing one Index from fastnotepad application exports.
    """  
    @staticmethod
    def mapSql(rec:list ):
        """
        maps the sql from the sqlite selector to the class.

        Args:
            rec (list): result of sqlite3 execute fetchall command

        Returns:
            NoteIndex: new noteindex class instance
        """        
        return NoteIndex(rec[0],rec[1],rec[2],rec[3],rec[6],rec[4],rec[5],rec[7],rec[8])
    
    def __init__(self, 
                 _key, 
                 _epochtime, 
                 _notelength, 
                 _preview, 
                 _folder = None, 
                 _sha256sum=None, 
                 _reviewed = False, 
                 _starred=False,
                 _complete=False):
        self.Key:str = _key
        self.EpochTime:float = _epochtime
        self.NoteLength:int = _notelength
        self.Preview:str = _preview
        self.Sha256Sum  = _sha256sum
        self.Reviewed = _reviewed
        self.Folder = _folder
        self.Starred = _starred
        self.Complete = _complete

    @staticmethod
    def makeNew(s:"sqlitestoremanager"):
        sql = "select 1 from noteindexes where [key]=?"

        db = s.OpenDb()

        newkey = generateAlphaNumeric(16)

        while len(db.execute(sql,(newkey,)).fetchall()) > 0:
            newkey = generateAlphaNumeric()
        
        return newkey 


    def Insert(self, s:"sqlitestoremanager"):
        s.InsertIndex(self.Key,
                      self.EpochTime,
                      self.NoteLength,
                      self.Preview,
                      self.Sha256Sum, 
                      self.Folder, 
                      self.Starred,
                      self.Complete)

class NoteContent:

    @staticmethod
    def mapSql(rec:list):
        return NoteContent(rec[0],rec[1],rec[2],rec[3])
    
    def __init__(self,_key, _contents, _scrollinfo,_sha256Sum):
        self.Key:str = _key
        self.Contents:str = _contents
        self.ScrollInfo:str = _scrollinfo
        self.Sha256Sum:str  = _sha256Sum

    def Insert(self, s:"sqlitestoremanager"):
        s.InsertContent(self.Key,
                        self.Contents,
                        self.ScrollInfo, 
                        self.Sha256Sum)
    
class NoteIndexUpdate:

    @staticmethod
    def mapSql(rec:list):
        return NoteIndexUpdate(rec[0],rec[1],rec[2],rec[3],rec[4],rec[7],rec[5],rec[6],rec[9],rec[8],rec[10])

    def __init__(self,
                 _updatekey, 
                 _key, 
                 _updatetime, 
                 _epochtime, 
                 _notelength, 
                 _folder = None, 
                 _preview=None,
                 _sha256Sum=None, 
                 _reviewed=False,
                 _starred=False,
                 _complete = False):
        
        self.UpdateKey:str = _updatekey
        self.Key:str = _key
        self.UpdateTime:float = _updatetime
        self.EpochTime:float = _epochtime
        self.NoteLength:int = _notelength
        self.Preview:str = _preview
        self.Sha256Sum:str = _sha256Sum
        self.Reviewed:bool = _reviewed
        self.Folder:str = _folder
        self.Starred = _starred
        self.Complete = _complete

    def makeNew(self,s:"sqlitestoremanager"):
        self.UpdateTime = datetime.datetime.now().timestamp()
        self.UpdateKey = str(s.makeKey("UPDATEKEY" ,"NOTEINDEXES_UPDATES"))

    def Insert(self, s:"sqlitestoremanager"):
        s.InsertIndexUpdate(self.UpdateKey,
                            self.Key,
                            self.UpdateTime, 
                            self.EpochTime,
                            self.NoteLength,
                            self.Preview,
                            self.Sha256Sum, 
                            self.Folder, 
                            self.Starred,
                            self.Complete,
                            self.Reviewed)

class NoteContentUpdate:

    @staticmethod
    def mapSql(rec:list):
        return NoteContentUpdate(rec[0],rec[1],rec[2],rec[3],rec[4],rec[5])

    def __init__(self,_updatekey, _key, _updatetime,  _contents, _scrollinfo,_sha256Sum=None):
        self.UpdateKey:str = _updatekey
        self.Key:str = _key
        self.UpdateTime:float = _updatetime
        self.Contents:str = _contents
        self.ScrollInfo:str = _scrollinfo
        self.Sha256Sum = _sha256Sum
    
    def Insert(self, s:"sqlitestoremanager"):
        s.InsertContentUpdate(self.UpdateKey,self.Key, self.UpdateTime, self.Contents,self.ScrollInfo,self.Sha256Sum)
    
    def makeNew(self,s:"sqlitestoremanager"):
        self.UpdateTime = datetime.datetime.now().timestamp()
        self.UpdateKey = str(s.makeKey("UPDATEKEY" ,"NOTECONTENTS_UPDATES"))

class InformationClasses:
    def __init__(self, _key, _name, _code) -> None:
        self.Key = _key
        self.Name = _name
        self.Code = _code

class sqlitestoremanager:
    
    """
    Manages the i/o to the sqlite database. the login this class
    assumes that the export files you provide will be imported in order.
    or that you will provide a reference by updatetime to ensure the 
    indexes and their updates match the content updates.
    """

    def GetClasses(self):

        getclass = 'select [key],name,code from classlookup order by [key]'
        db = self.OpenDb()

        res = db.execute(getclass).fetchall()

        return [InformationClasses(key,name,code) for key,name,code in res]


    def Statistics_Exists(self,_key) ->bool:
        existssql = f"select 1 from statistics where key='{_key}'"
        db = self.OpenDb()

        rec = db.execute(existssql).fetchall()

        return len(rec) > 0

    def getKeyList(self, filters=None):
        db = self.OpenDb()
        
        rows = None

        if filters is None:
            rows = db.execute('select [key] from noteindexes order by epochtime').fetchall()
        else:
            er = filters['exclude_reviewed'][0]
            es = filters['exclude_hasStatistics'][0]
            ec = filters['exclude_hasClass'][0]
            sd = filters['startDate'][0]
            ed = filters['endDate'][0]
            st:str = filters['searchText'][0]

            keywordlist = []
            likephrase = ""

            if st != "":
                likephrase = "and ()"

                keywordlist = st.split(" ")

                for k in keywordlist:
                    likephrase = likephrase + "Contents like '%{k}%' or"
                
                likephrase = likephrase [:-2]+")"

            sql = self.get_key_list + likephrase + "order by "

            filters = {
                'noST': sd==0,
                'noET': ed==0,
                'excludeifStats': es,
                'excludeReviewed':er,
                'excludeClass':ec,
                'startTime':sd,
                'endTime':ed
            }

            rows = db.execute(self.get_key_list,filters).fetchall()

        return [id for id, in  rows]

    def GetStatistics(self, _key):
        db = self.OpenDb()

        stats = db.execute(self.select_statistics,(_key,)).fetchone()

        if stats is None:
            return None
        else:
            return Statistics.mapSql(stats)
        
    def AddOrUpdateStatistics(self, _key,_killings,_saved,_drugged,_thefts, _informed):
        existssql = f"select 1 from statistics where key='{_key}'"
        db = self.OpenDb()

        rec = db.execute(existssql).fetchall()

        if (len(rec)>0):
            db.execute( self.update_statistics, (_saved,_killings,_drugged,_thefts,_informed,_key))
        else:
            db.execute( self.insert_statistics, (_key, _killings,_saved, _drugged, _thefts, _informed))
        
        db.commit()

    def getClassifications(self, key:str):
        sql = f"select classkey from classification where [key]='{key}'"

        db = self.OpenDb()

        items = db.execute(sql).fetchall()
        
        classes = []

        for i in items:
            classes.append(i[0])

        return classes

    def setClassifications(self, key:str, clist:list[int]):
        setarg = ""

        for c in clist:
            setarg= setarg + f"{c}, "
        
        # chop off comma
        setarg = setarg[0:len(setarg)-2]
        setarg = "(" + setarg+")"

        # delete any classifiers that have been cleared
        delsqll = f" delete from classification where key='{key}' and not classkey in {setarg}"
        
        db = self.OpenDb()

        db.execute(delsqll)
        db.commit()

        # get a list of remaining classifications for the specified key 
        selsqk = f" select classkey from classification where key='{key}' and classkey in {setarg}"
        insclas = " insert into classification values \n"
        indb = db.execute(selsqk).fetchall()

        # subtract the keys that already exist.
        for i in indb:
            if i[0] in clist:
                clist.remove(i[0])

        # if there are any left build an insert statement an execute
        if len(clist) > 0:
            vals = ""

            for c in clist:
                insclas = insclas + f"('{key}',{c}),\n"
            
            insclas = insclas[0:len(insclas)-2]

            db.execute(insclas)
            db.commit()
   
    def __init__(self, emptypath, outputpath) -> None:
        self.empty_db_path = emptypath
        self.output_db_path = outputpath

        if not pathlib.Path(outputpath).exists():
            filecopy(self.empty_db_path,self.output_db_path) 

        self.connection:sqlite3.Connection = None
        """
        Singleton connection object
        """

        self.get_key_list = readall(dir.joinpath("get_key_list.sql"))
        self.select_statistics = readall(dir.joinpath("select_statistics.sql"))
        self.insert_statistics = readall(dir.joinpath("insert_statistics.sql"))
        self.update_statistics = readall(dir.joinpath("update_statistics.sql"))
        
        self.update_index_shasum = readall(dir.joinpath("update_index_shasum.sql"))
        self.update_index_update_shasum = readall(dir.joinpath("update_index_update_shasum.sql"))
        self.update_index_flags = readall(dir.joinpath("update_index_flags.sql"))

        self.insert_content_sql = readall( dir.joinpath("insert_contents.sql"))
        self.insert_index_sql = readall(dir.joinpath("insert_index.sql"))
        self.select_contents_by_key = readall(dir.joinpath("select_contents_by_key.sql"))
        self.select_index_by_key = readall(dir.joinpath("select_index_by_key.sql"))
     
        self.insert_contents_updates = readall(dir.joinpath("insert_contents_updates.sql"))
        self.insert_index_updates = readall(dir.joinpath("insert_index_updates.sql"))
        
        self.select_index_updates = readall(dir.joinpath("select_index_updates_by_key.sql"))
        self.select_contents_updates = readall(dir.joinpath("select_contents_updates_by_key.sql"))
 
    def makeKey(self,field:str,table:str)->str:
        """
        Generates a UUID for a database field until its unique

        Args:
            field (str): field to generate the uuid for
            table (str): table of the field to generate the uuid for

        Returns:
            str: the new uuid
        """
        db = self.OpenDb()
        checksql = fieldexistssql(field,table)
        newkey:str = uuid.uuid4().hex

        while True:
            keyexist = db.execute(checksql,(newkey,)).fetchone()
            if keyexist[0]==0:
                break
            else:
                newkey = uuid.uuid1().hex
        
        return newkey

    def OpenDb(self)->sqlite3.Connection:
        """
        Acts like a singleton, sqlite only allows one write thread, and 
        returns an open connection to the configured sqlite database.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.output_db_path)
        
        return self.connection

    def GetIndex(self,key:str) -> tuple[NoteIndex, list[NoteIndexUpdate]] :
        """
        Returns a tuple containing the matching NoteIndex record and a list of NoteIndex updates

        Args:
            key (str): key to retrieve

        Returns:
            tuple(NoteIndex,list(NoteIndexUpdate)): all entries matching the key
        """
        db = self.OpenDb()

        cursor = db.execute(self.select_index_by_key,(key,))
        index = cursor.fetchone()

        if index is not None:
            index = NoteIndex.mapSql(index)

        cursor = db.execute(self.select_index_updates,(key,))
        updates = cursor.fetchall()

        if len(updates )>0:
            outrecs = []

            for i in updates:
                outrecs.append(NoteIndexUpdate.mapSql(i))

            updates = outrecs

        return (index,updates)
        
    def GetContents(self,key):
        db = self.OpenDb()
        
        cursor = db.execute(self.select_contents_by_key,(key,))
        contents = cursor.fetchone()
        

        if contents is not None:
            contents = NoteContent.mapSql(contents)

        cursor = db.execute(self.select_contents_updates, (key,))
        updates = cursor.fetchall()

        if len(updates )>0:
            outrecs = []

            for i in updates:
                outrecs.append(NoteContentUpdate.mapSql(i))

            updates = outrecs

        return (contents,updates)

    def InsertIndex(self, _key, _epochtime, _notelength, _preview,_sha256sum,_folder,_starred,_complete):
        if _folder is not None and  _folder.strip(' ') == '':
            _folder = None

        rec = (_key, _epochtime, _notelength, _preview,_sha256sum,_folder,_starred,_complete)
        db = self.OpenDb()

        db.execute(self.insert_index_sql,rec)
        db.commit()

    def InsertIndexUpdate(self, _updatekey, _key, _updatetime, _epochtime, _notelength, _preview,_sha256sum,_folder,_starred,_complete,_reviewed):
        if _folder is not None and  _folder.strip(' ') == '':
            _folder = None

        rec = (_updatekey, _key, _updatetime,_epochtime, _notelength, _preview, _sha256sum,_folder,_starred,_complete,_reviewed)
        db = self.OpenDb()

        db.execute(self.insert_index_updates,rec)
        db.commit()

    def InsertContent(self, _key, _contents, _scrollinfo,_sha256sum):
        rec = (_key, _contents, _scrollinfo,_sha256sum)
        db  = self.OpenDb()

        db.execute(self.insert_content_sql,rec)
        db.commit()

    def InsertContentUpdate(self, _updatekey:str, _key:str, _updatetime:float,  _contents:str, _scrollinfo:str, _sha256Sum):
        rec = (_updatekey, _key, _updatetime,  _contents, _scrollinfo,_sha256Sum)
        db  = self.OpenDb()

        db.execute(self.insert_contents_updates,rec)
        db.commit()

    def UpdateIndexShaSum(self, indexbinder,  _Sha256Sum=None, updatetime = None ):

        db = self.OpenDb()

        if indexbinder[0] is None: 
            raise "You need to call GetIndex() prior to calling this function and pass its result"
        
        key = indexbinder[0].Key

        if len(indexbinder[1]) > 0:

            for cu in indexbinder[1]:
                c:NoteIndexUpdate = cu
                if (c.UpdateTime == updatetime):
                    sql = self.update_index_update_shasum
                    db.execute(sql,(_Sha256Sum,key,updatetime))
                    db.commit()
                    break
        else:
            sql = self.update_index_shasum
            db.execute(sql, (_Sha256Sum,key))
            db.commit()

    def AddOrUpdateIndex(self,  _key:str, _epochtime:float, _notelength:int, _preview:str, _folder:str, _starred:int, _complete:int, _reviewed:int):
        """
        This adds or updates an existing index by key to keep track of 
        changes to existing records while preserving the earlier ones 
        designed this way as fastnotepad will overwrite existing 
        records if the user changes them. This should be called  
        before AddOrUpdateContent. 

        Args:
            _key (_type_): _description_
            _epochtime (_type_): _description_
            _notelength (_type_): _description_
            _preview (_type_): _description_

        Returns:
            float: returns the update time of the new record
        """  

        db = self.OpenDb()

        if _folder is not None and _folder.strip(' ') == '':
            _folder = None

        indexbinder:tuple[NoteIndex, list[NoteIndexUpdate]] = self.GetIndex(_key)
        indexrec:NoteIndex = indexbinder[0]
        indexupdates:list[NoteIndexUpdate] = indexbinder[1]

        if indexrec is None:
             irec:NoteIndex = NoteIndex(_key,_epochtime,_notelength,_preview,_folder, None,_reviewed,_starred,_complete)   
             irec.Insert(self)

             return irec.EpochTime
        else:
            if indexrec.EpochTime == _epochtime and indexrec.Folder==_folder:
                        # and indexrec.Starred == _starred and \
                        # indexrec.Complete == _complete :
                print(f"duplicate index {_key}")
                
                db.execute(self.update_index_flags, (_starred, _complete,_key))
                db.commit()
                
                return _epochtime
            else:      
                for c in indexupdates:  
                    if c.UpdateTime == _epochtime and \
                       c.Folder == _folder and \
                       c.Starred == _starred:

                        db.execute(self.update_index_flags, (_starred, _complete,_key))
                        db.commit()

                        print(f"duplicate index update {_key}")
                        return _epochtime
                
                iupdate:NoteIndexUpdate = NoteIndexUpdate("",_key,0,indexrec.EpochTime,_notelength,_folder,_preview,None, _reviewed,_starred,_complete)
                iupdate.makeNew(self)
                iupdate.UpdateTime = _epochtime
                iupdate.Insert(self)

                return iupdate.UpdateTime
          
    def AddOrUpdateContents(self,_key, _contents, _scrollinfo, _updatetime=-1, _sha256Sum=None):
        """
         Checks for key, also checks if the string is unique in
        existing content updates. If the key exists, it will 
        add the record as an update record, or if the content 
        does not yet exist as a content record.
        If the key does not exist it will attempt to creatse a new
        index from the provided content.

        Args:
            _key (_type_): _description_
            _contents (_type_): _description_
            _scrollinfo (_type_): _description_
            _updatetime (float, optional): allows specific updatecontent record to be referenced. Defaults to -1.
        """
        # gets the index record if it exists
        indexbinder:tuple[NoteIndex, list[NoteIndexUpdate]] = self.GetIndex(_key)

        indexrec:NoteIndex = indexbinder[0]
        indexupdates:list[NoteIndexUpdate] = indexbinder[1]

        contentbinder:tuple[NoteContent, list[NoteContentUpdate]] = self.GetContents(_key)
        
        contentrec:NoteContent = contentbinder[0]
        contentupdates:list[NoteContentUpdate] = contentbinder[1]
        
        updatecountequal = len(contentupdates) == len(indexupdates)

        if (_sha256Sum is None):
            _sha256Sum = hashlib.sha256(_contents.encode('utf-8')).hexdigest()
        
        if indexrec is not None:

            # update shasum in index.
            self.UpdateIndexShaSum(indexbinder,_sha256Sum, _updatetime )

            # only occurs if this key has nothing associated.
            if contentrec is None:
                crec:NoteContent = NoteContent(_key,_contents,_scrollinfo, _sha256Sum)
                crec.Insert(self)
            else:
                if updatecountequal:
                   
                    if _updatetime == indexrec.EpochTime:
                       print('skipping duplicate content.')
                       return
                    
                    for c in contentupdates:
                        if c.UpdateTime == _updatetime:
                            print('skipping duplicate content')
                            return
                else:

                    if _updatetime == -1:
                        raise "you have to provide an update time when adding a contentupdate that matches the index\n check your code."
                    
                    crec:NoteContentUpdate = NoteContentUpdate("",_key,_updatetime,_contents,"")
                    
                    matchingIndexUpdate = None

                    for i in indexupdates:
                        curr:NoteIndexUpdate = i
                        if curr.UpdateTime == _updatetime:
                            matchingIndexUpdate = curr
                            break
                    
                    if matchingIndexUpdate is None:
                        raise "There was no index update, call addorupdateindex first !"

                    crec.UpdateKey = curr.UpdateKey
                    crec.Sha256Sum = _sha256Sum
                   
                    crec.Insert(self)    
        else:
            raise "call AddOrUpdateIndex first !"
                




    

        
