INSERT INTO NoteIndexes (
                            [Key],
                            EpochTime,
                            NoteLength,
                            Preview,
                            Sha256Sum,
                            Folder,
                            Starred,
                            Complete,
                            FileSource

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
                            ?
                        );
