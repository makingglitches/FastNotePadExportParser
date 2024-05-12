INSERT INTO NoteContents_Updates (
                                     UpdateKey,
                                     [Key],
                                     UpdateEpoch,
                                     Contents,
                                     ScrollInfo,
                                     Sha256Sum
                                 )
                                 VALUES (
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                     ?
                                 );
