SELECT count([key]),
       sum(SavedCount) as scount,
       sum(KillingsCount) as kcount,
       sum(DruggingsCount) as dcount,
       sum(TheftsCount) as tcount,
       sum(InformedCount) as icount
  FROM Statistics