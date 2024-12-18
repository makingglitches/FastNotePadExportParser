SELECT UpdateKey,
       "Key",
       UpdateTime,
       EpochTime,
       NoteLength,
       Folder,
       Preview,
       Sha256Sum,
       Reviewed,
       Starred,
       Complete,
       FileSource,
       NoContent
from NoteIndexes_Updates where key=?
order by updatetime desc limit 1;