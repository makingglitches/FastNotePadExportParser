UPDATE NoteIndexes_Updates
   SET UpdateKey = :UpdateKey,
       [Key] = :Key,
       UpdateTime = :UpdateTime,
       EpochTime = :EpochTime,
       NoteLength = :NoteLength,
       Preview = :Preview,
       Sha256Sum = :Sha256Sum,
       Reviewed = :Reviewed,
       Folder = :Folder,
       Starred = :Starred,
       Complete = :Complete,
       FileSource = :FileSource,
       NoContent = :NoContent
 WHERE UpdateKey = :UpdateKey;