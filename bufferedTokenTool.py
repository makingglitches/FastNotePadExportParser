from io import TextIOWrapper

class bufferedTokenTool:

    def __init__(self,filename:str, _buffersize = 1024) -> None:
        self.FileName = filename
        self.fileptr:TextIOWrapper = None
        self.buffersize = _buffersize
        self.startI=0
        self.currentbuffer:str = ""


    def open(self):
        self.fileptr = open(self.FileName, "r")

    def close(self):
        if self.fileptr:
            self.fileptr.close()

    def IfNeededGrabNextBuffer(self):
          if not self.currentbuffer or self.startI == len(self.currentbuffer):
                self.currentbuffer = self.fileptr.read(self.buffersize)
                self.startI = 0

                if not self.currentbuffer:
                    raise ValueError("could not find value")


    def advanceTo(self, str, str1 = None):
        """
        starting at current startI location, copy the characters in the buffer
        continuing until either the first or second search character is encountered
        and return that character as well. 

        Args:
            str (str): first character to search for
            str1 (str): second character to search for. Defaults to None.

        Raises:
            ValueError: the value could not be found before end of file

        Returns:
            str: the value extracted
        """

    
        currstr = ""

        # check if the current buffer index is beyond the end of buffer
        # if so read more data from file and reset index to beginning.
        self.IfNeededGrabNextBuffer()
        
        # check if either of the strings match the first value position
        # if so return the value and advance the index
        # if self.currentbuffer[self.startI] == str or self.currentbuffer[self.startI] == str1:
        #     currstr = str if self.currentbuffer[self.startI] == str else str1 
        #     self.startI= self.startI+1
        #     return currstr

        # there is no do-while in python... 
        while True:
            
            self.IfNeededGrabNextBuffer()

            # grab current character
            currstr = currstr + self.currentbuffer[self.startI]
            
            self.startI = self.startI + 1

            # the file is very very bad.
            if  ((str == "\"" or str1=="\"") 
                  and currstr[len(currstr)-2:len(currstr)] == "\\\""): 
                continue
            
            #control character for record start can occur in files.
            if (str == "^" or str1=="^") and currstr[len(currstr)-1]=="^":
                self.IfNeededGrabNextBuffer()
                if self.currentbuffer[self.startI] != "!":
                    continue

            if (str == currstr[len(currstr)-1] or 
                ( str1 is not None and str1==currstr[len(currstr)-1])):
            #self.startI = self.startI + 1
                break


        
        return currstr
    


