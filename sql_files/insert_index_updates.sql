INSERT INTO NoteIndexes_Updates (
                                    UpdateKey,
                                    [Key],
                                    UpdateTime,
                                    EpochTime,
                                    NoteLength,
                                    Preview,
                                    Sha256Sum,
                                    Folder,
                                    Starred,
                                    Complete,
                                    Reviewed
                                )
                                VALUES (
                                     ?,
                                     ?,
                                     ?,
                                     ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?,
                                    ?
                                );
