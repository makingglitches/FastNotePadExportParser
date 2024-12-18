UPDATE NoteIndexes
   SET [Key] = :Key,
       EpochTime = :EpochTime,
       NoteLength = :NoteLength,
       Preview = :Preview,
       Sha256Sum = :Sha256Sum,
       Reviewed = :Reviewed,
       Folder = :Folder,
       Starred = :Starred,
       Complete = :Complete,
       FileSource = :FileSource
 WHERE "Key" = :Key;