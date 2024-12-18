import sqlitestoremgr

empty_db_path = "fastnoteparser/notedatabase_empty.sqlite"
output_db_path = "output/notedatabase.sqlite"


insert_stats_sql_path = str(sqlitestoremgr.dir.joinpath('insert_statistics.sql'))
update_indexes_reviewed_path = str(sqlitestoremgr.dir.joinpath("update_index_changereviewed.sql"))

insert_stats_sql_code = sqlitestoremgr.readall(insert_stats_sql_path)
update_indexes_reviewed_code = sqlitestoremgr.readall(update_indexes_reviewed_path)

sql = sqlitestoremgr.sqlitestoremanager(emptypath=empty_db_path,outputpath=output_db_path)
db = sql.OpenDb()


#MODIFIED chatgpt contributed code.
import csv
import os

print(os.getcwd())

# Specify the CSV file name
csv_file_name = '/home/john/Documents/placeflattener_git/input/toreview-4-20-2024.csv'

print( os.path.join(os.getcwd(), csv_file_name))

# Open the CSV file in read mode
with open(csv_file_name, 'r', newline='') as csv_file:
    # Create a CSV reader
    csv_reader = csv.reader(csv_file)

    # Skip the header
    header = next(csv_reader)

    # Connect to the SQLite database
    cursor = db.cursor()

    updated = 0
    skipped = 0
    reviewset = 0

    # Iterate through the rows in the CSV file
    for row in csv_reader:
        # Assuming the last four columns as kcount, scount, dcount, tcount, icount
        key_value = row[0]
        kcount = int(row[3])
        scount = int(row[4])
        dcount = int(row[5])
        tcount = int(row[6])
        icount = int(row[7])
        reviewed = 0 if row[8] == '' else int(row[8])

        if (reviewed > 0 ):
            cursor.execute(update_indexes_reviewed_code, (reviewed,key_value))
            reviewset = reviewset + 1
            
        # only insert a row if one doesn't exist, and only if there is a value with positive values.
        if (kcount >0 or scount >0 or dcount > 0 or tcount > 0 or icount > 0):
            # Generate and execute the INSERT statement
            cursor.execute(insert_stats_sql_code, (key_value,kcount,scount,dcount,tcount,icount))
            updated = updated + 1
        else:
            skipped = skipped + 1

    print(f"Updated: {updated}  Skipped: {skipped} ReviewSet {reviewset}")
    # Commit the changes and close the database connection
    db.commit()
    db.close()
