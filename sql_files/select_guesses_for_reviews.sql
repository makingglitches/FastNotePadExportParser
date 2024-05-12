select 
    ni.key, 
    ni.epochtime, 
    nc.contents, 
    0 as KCount, 
    0 as SCount, 
    0 as DCount,
    0 as TCount,
    0 as ICount,
    0 as Reviewed
    from NoteContents nc
    inner join NoteIndexes ni
    on ni.key = nc.key 
    where 
        (nc.Contents like '%plus%' or 
        nc.Contents like '%drugged%' or
        nc.Contents like '%steal%' or 
        nc.Contents like '%stolen%') and 
        not EXISTS (select 1 from statistics s where s.key=ni.key)
        and ni.Reviewed =0 