SELECT
UpdateKey,
[Key],
UpdateEpoch,
Contents,
ScrollInfo,
Sha256Sum,
FileSource

  FROM NoteContents_Updates
  where [key] = ?
  order by updateepoch desc 
  limit 1;