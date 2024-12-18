import sqlitestoremgr
import datetime

empty_db_path = "fastnoteparser/notedatabase_empty.sqlite"
output_db_path = "output/notedatabase.sqlite"

guess_sql_path = str(sqlitestoremgr.dir.joinpath('select_guesses_for_reviews.sql'))
sql = sqlitestoremgr.sqlitestoremanager(emptypath=empty_db_path,outputpath=output_db_path)
db = sql.OpenDb()

guess_sql_code = sqlitestoremgr.readall(guess_sql_path)

# this code contributed by chatgpt and altered
import csv


# Connect to the SQLite database
cursor = db.cursor()

# Execute your query
cursor.execute(guess_sql_code)
result = cursor.fetchall()

dnow = datetime.datetime.now()
# Specify the CSV file name
csv_file_name = f'output/toreview-{dnow.month}-{dnow.day}-{dnow.year}.csv'

# Open the CSV file in write mode
with open(csv_file_name, 'w', newline='') as csv_file:
    # Create a CSV writer
    csv_writer = csv.writer(csv_file)

    # Write the header (column names)
    csv_writer.writerow([description[0] for description in cursor.description])

    # Write the data
    csv_writer.writerows(result)

# Close the database connection
db.close()


