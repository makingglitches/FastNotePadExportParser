INSERT INTO Files (
                      Sha256Sum,
                      FileName,
                      Date,
                      ExportNumberOnDate,
                      MainSourceFile,
                      RunDate
                  )
                  VALUES (
                      ?,
                      ?,
                      ?,
                      ?,
                      ?,
                      ?
                  );
