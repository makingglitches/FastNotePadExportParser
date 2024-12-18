SELECT "Key",
       Contents,
       ScrollInfo,
       Sha256Sum,
       FileSource
  FROM NoteContents
  where Key = :Key;