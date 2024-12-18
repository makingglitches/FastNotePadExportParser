SELECT "Key",
       SavedCount,
       KillingsCount,
       DruggingsCount,
       TheftsCount,
       InformedCount,
       FamilyKilled,
       BitBySnakeCount,
       FileSource
  FROM Statistics
where key = ?