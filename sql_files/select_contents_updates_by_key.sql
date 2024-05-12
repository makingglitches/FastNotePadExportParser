SELECT
UpdateKey,
[Key],
UpdateEpoch,
Contents,
ScrollInfo,
Sha256Sum

  FROM NoteContents_Updates
  where [key] = ?
  order by updateepoch desc 