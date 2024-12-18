select 
[Key],
EpochTime,
NoteLength,
Preview,
Sha256Sum,
Reviewed,
Folder,
Starred,
Complete,
FileSource
from NoteIndexes where [Key] = ?
