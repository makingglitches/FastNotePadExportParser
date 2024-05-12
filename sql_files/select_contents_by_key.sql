 select 
    [Key],
    Contents,
    ScrollInfo,
    Sha256Sum
from NoteContents where Key = ?    
 