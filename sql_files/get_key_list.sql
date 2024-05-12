select ni."Key" from noteindexes ni
inner join notecontents nu 
on nu."Key" = ni."Key"
where ((:noST or ni.EpochTime >= :startTime) 
and  (:noET or ni.EpochTime <= :endTime) or exists
(select 1 from noteindexes_updates nui where 
  (:noST or nui.UpdateTime >= :startTime) and
  (:noET or nui.UpdateTime <= :endTime)  and nui."Key"=ni."Key")) and 
  ( (not :excludeifStats) or 
      (:excludeifStats and  
          not exists (select 1 from statistics st where ni."Key"))) and
  ( (not :excludeReviewed) or  (:excludeReviewed and not ni.Reviewed)) and 
  ( (not :excludeClass) or (:excludeClass and not exists (select 1 from
  classification c where c."Key" = ni."Key"))) 
