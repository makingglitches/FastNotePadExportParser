import bufferedTokenTool

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

    def __init__(self, filename: str, _buffersize=1024,_verbose = False) -> None:
        self.btt = bufferedTokenTool.bufferedTokenTool(filename,_buffersize)
        self.OnIRecord = print
        self.OnCRecord = print
        self.OnFileId = print
        self.Verbose = _verbose

    def printrecord(self,record:list, number:int):
        print(f"==========Record: {number}===========")
        
        for i in range(0,len(record)):
            print(f"Field #{i}: {record[i]}")

    def run(self):
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

            rec = []
            print(recnum)

            # get record fields for first 9 fields
            for i in range(1,10):
                nextfield = btt.advanceTo(";").replace("!","").replace("^","").replace(";","")
                rec.append(nextfield)

            # get last field which is preview.
            #wrong, allow for special characters elsewhere.
            #nextfield = btt.advanceTo("^","\"").replace("^","")
            nextfield = btt.advanceTo("^","\"")

            if nextfield[len(nextfield)-1]=="^":
                nextfield = nextfield[0:len(nextfield)-1]
            
            rec.append(nextfield)

            if self.Verbose:
               self.printrecord(rec,recnum)
    
            recnum = recnum + 1 

            if self.OnIRecord:
                self.OnIRecord(recnum,rec)

            if not nextfield.endswith("\\\"") and nextfield.endswith("\""):
                endbracket = btt.advanceTo("}")
                if self.Verbose:
                    print("=============== end reached ==============")
                break

        tokenconst = "{[!*|@]}{}{[!*|@]}{"
        tokenstr = ""

        while (tokenstr != tokenconst):
            tokenstr = tokenstr+ btt.advanceTo("{")

        if self.Verbose:
            print(tokenstr)
            print(f"found {recnum} indices")

        recnum = 0

        while True:
            rec = []

            # id field
            nextfield = btt.advanceTo(":").replace("\"","").replace("_","").replace(":","")
            rec.append(nextfield)

            #contents field
            nextfield = btt.advanceTo("\"") + btt.advanceTo("\"") + btt.advanceTo(",","}")
            endbracket = nextfield[len(nextfield)-1] == "}"
            nextfield = nextfield[1:len(nextfield)-2] if len(nextfield) > 3 else nextfield
            rec.append(nextfield)

            # in the proper ordering of things this only happens at the end of the file.
            if endbracket:
                rec.append("")
              
                if self.Verbose:
                      self.printrecord(rec,recnum)
                      print("==============end record contents ==========")
              
                if self.OnCRecord:
                    self.OnCRecord(recnum,rec)
              
                break

            nextfield = ""

            astr = btt.advanceTo("_")
            
            #there are sometimes multiple goddamn scrollY fields, condense them to 1
            while ("ScrollY" in astr):
                astr = astr + btt.advanceTo(',','0').replace(":0","").replace(',',"")
                nextfield = nextfield + astr
                astr = btt.advanceTo("_","}")
            
            rec.append(nextfield)

            if self.OnCRecord:
                self.OnCRecord(recnum,rec)

            if self.Verbose:
                self.printrecord(rec,recnum)

            recnum = recnum+1

            if '}' in astr:
                print("==============end record contents ==========")
                break

        print(f"found {recnum} record contents")

        btt.close()
                
            
