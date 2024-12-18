 select 
    [Key],
    Contents,
    ScrollInfo,
    Sha256Sum,
    FileSource
from NoteContents where Key = :Key   
 