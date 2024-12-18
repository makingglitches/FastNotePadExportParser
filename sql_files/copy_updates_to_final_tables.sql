INSERT INTO UnifiedContentUpdates 
(
   UpdateKey,
   [Key],
   UpdateEpoch,
   Contents,
   Sha256Sum,
   EpochTime,
   NoteLength,
   Reviewed,
   Folder,
   Starred,
   Complete,
   FileSource
)
select i.UpdateKey,
       i."Key", 
       i.UpdateTime, 
       u.Contents, 
       i.Sha256Sum,
       i.EpochTime,
       i.NoteLength,
       i.Reviewed,
       i.Folder,
       i.Starred,
       i.Complete,
       i.FileSource
from noteindexes_updates i 
inner join notecontents_updates u 
on i.UpdateKey = u.UpdateKey
where not exists (select null from unifiedcontentupdates uc where 
uc.UpdateKey = i.UpdateKey)