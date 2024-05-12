SELECT 
UpdateKey,
[Key],
UpdateTime,
EpochTime,
NoteLength,
Preview,
Sha256Sum,
Folder,
Starred,
Reviewed,
Complete
  FROM NoteIndexes_Updates
  where [key] = ?
  order by updatetime desc