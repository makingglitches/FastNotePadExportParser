import bufferedTokenTool
import json

class fastNoteTool:
    """
    Intended for forward read of a FastNotePad export file
    Calls two event handlers with a recordnumber and list as the only arguments
    Calls an additional event handler to return the file record number
    """    

    OnIRecord= print
    """
    Called when the run() method discovers a record of Index type
    """    

    OnCRecord= print
    """
    Called when the run() method discovers record of Content type
    """    

    OnFileId= print
    """
    Called when the run() method discovers the file id
    """

    Verbose:bool

    def __init__(self, filename: str, sha, _buffersize=1024,_verbose = False, ) -> None:
        self.btt = bufferedTokenTool.bufferedTokenTool(filename,_buffersize)
        self.OnIRecord = print
        self.OnCRecord = print
        self.OnFileId = print
        self.Verbose = _verbose
        self.Folders = []
        self.FileSource = sha

    def printrecord(self,record:list, number:int):
        print(f"==========Record: {number}===========")
        
        for i in range(0,len(record)):
            print(f"Field #{i}: {record[i]}")

    def run(self):

       

        print('Processing Indexes')
        
        btt = self.btt

        btt.open()
            
        # get the file id 
        fileid = btt.advanceTo("#").replace("#","")

        if self.OnFileId:
            self.OnFileId(fileid)

        #find start of indexes string
        indexstr = btt.advanceTo(":")
        indexstr = indexstr+btt.advanceTo("\"")

        if indexstr == "{\"index\":\"":
            if self.Verbose:
                print("Parsing Indexes and timestamps.")
        else:
            raise IOError("Index block not found, invalid file structure")

        # advance to first record
        startrec = btt.advanceTo("^")

        recnum = 0

        while True:

            rec = {}
            trec = []
            if self.Verbose:
                print(recnum)

            # get record fields for first 9 fields
            for i in range(1,10):
                nextfield = btt.advanceTo(";").replace("!","").replace("^","").replace(";","")
                trec.append(nextfield)
            
            # get last field whicj is preview.
            #wrong, allow for special characters elsewhere.
            #nextfield = btt.advanceTo("^","\"").replace("^","")
            nextfield = btt.advanceTo("^","\"")

            if nextfield[len(nextfield)-1]=="^":
                nextfield = nextfield[0:len(nextfield)-1]
            
            trec.append(nextfield)

            rec['key']=trec[0]
            rec['epochtime']=float(trec[3])
            rec['notelength'] = int(trec[6])
            rec['preview'] = trec[9]
            rec['folder'] = trec[1]
            rec['starred'] = True if trec[7] == '1' else False
            rec['complete'] = True if trec[4] == 'i2' else False

            if self.Verbose:
               self.printrecord(rec,recnum)
    
            recnum = recnum + 1 

            if self.OnIRecord:
                self.OnIRecord(recnum,rec, self.FileSource)

            if not nextfield.endswith("\\\"") and nextfield.endswith("\""):
                endbracket = btt.advanceTo("}")
                if self.Verbose:
                    print("=============== end reached ==============")
                break

        
        tokenconst = "{[!*|@]}"
        tokenstr = ""

        print('Processing Contents')

        # there can be two of the tokenconst's which surround a list of 
        # folder names.
        while (tokenstr != tokenconst):
            tokenstr = tokenstr+ btt.advanceOne()

        nextfield = btt.advanceOne(3)

        if nextfield == "{\"f":
            nextfield = nextfield + btt.advanceTo("}")
            self.Folders =  json.loads(nextfield)["folders"].split('\n')

            nextfield = btt.advanceTo("}")
            if nextfield != tokenconst:
                raise f"malformed file, expected sections token: {tokenconst} \n got {nextfield}"

        else:
            # advance to next token constant instance.
            nextfield = nextfield + btt.advanceTo("}")
            if nextfield != "{}"+tokenconst:
                raise f"malformed file, should have found empty folders list and token constant."

            self.Folders = []


        if self.Verbose:
            print(tokenstr)
            print(f"found {recnum} indices")

        recnum = 0

        while True:
            rec = {}

            # id field
            nextfield = btt.advanceTo(":").replace("\"","").replace("_","").replace(":","")
            rec['key'] = nextfield
            #rec.append(nextfield)

            #contents field
            nextfield = btt.advanceTo("\"") + btt.advanceTo("\"") + btt.advanceTo(",","}")
            endbracket = nextfield[len(nextfield)-1] == "}"
            nextfield = nextfield[1:len(nextfield)-2] if len(nextfield) > 3 else nextfield
            rec['contents'] = nextfield
            #rec.append(nextfield)

            # in the proper ordering of things this only happens at the end of the file.
            if endbracket:
                rec['scrolly']="" 
                if self.Verbose:
                      self.printrecord(rec,recnum)
                      print("==============end record contents ==========")
              
                if self.OnCRecord:
                    self.OnCRecord(recnum,rec, self.FileSource)
              
                break

            nextfield = ""

            astr = btt.advanceTo("_")
            
            #there are sometimes multiple goddamn scrollY fields, condense them to 1
            while ("ScrollY" in astr):
                astr = astr + btt.advanceTo(',','0').replace(":0","").replace(',',"")
                nextfield = nextfield + astr
                astr = btt.advanceTo("_","}")
            rec['scrolly'] = nextfield
            #rec.append(nextfield)

            if self.OnCRecord:
                self.OnCRecord(recnum,rec, self.FileSource)

            if self.Verbose:
                self.printrecord(rec,recnum)

            recnum = recnum+1

            if '}' in astr:
                if self.Verbose:
                    print("==============end record contents ==========")
                break

        print(f"found {recnum} records")

        btt.close()
                
            
