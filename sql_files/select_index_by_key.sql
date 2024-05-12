select 
[Key],
EpochTime,
NoteLength,
Preview,
Sha256Sum,
Reviewed,
Folder,
Starred,
Complete
from NoteIndexes where [Key] = ?
