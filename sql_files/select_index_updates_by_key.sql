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
  FROM NoteIndexes_Updates
  where [key] = ?
  order by updatetime desc