insert into UnifiedContent ("Key",
                            EpochTime,
                            NoteLength,
                            Sha256Sum,
                            Folder,
                            Starred,
                            Reviewed,
                            Complete,
                            Contents,
                            FileSource )
select i."Key",
       i.EpochTime,
       i.NoteLength,
       i.Sha256Sum,
       i.Folder,
       i.Starred,
       i.Reviewed,
       i.Complete,
       c.Contents,
       i.FileSource
from noteindexes i
inner join notecontents c
on c."Key" = i."Key"
WHERE NOT EXISTS (SELECT  NULL FROM UNIFIEDCONTENT U WHERE U."Key" = i."Key")