import pg8000 as pg
import csv
import psycopg2 as ps2

#Using the names of the files
filename_list = [
    'id', 'first_name', 'last_name', 'email', 'gender', 'ip_address', 'plant_specific']
pg_username = 'postgres' #TO ENTER
pg_password = '19019355' #TO ENTER
pg_database = 'lego_manufacturing'

print("Connection Successful!")

#i do this for all filetypes
data_dict = dict()
#Open csv files and store data in a dictionary that is called by the filename.
for file in filename_list:
    with open('data/MOCK_DATA.csv', newline='', encoding='utf-8') as csvfile:
        fileData = []
        readCSV = csv.reader(csvfile)
        for row in readCSV:
            fileData.append(row)
    data_dict[file] = fileData
counter = 0
for key, value in data_dict.items():
    newlist = []
    for v in value:
        for element in v:
            rowList = element.split(',')
            if '' in rowList:
                counter += 1
                print(element)
                continue
            newlist.append(rowList)
    data_dict[key] = newlist
del newlist[0]
# [row for row in newlist if row[x].isdigit()]
for n in newlist:
    print(n)
print(len(newlist))
print('you lost {} rows of data'.format(counter))

#connect to database.
#conn = pg.connect(user=pg_username, password=pg_password)
conn = pg.connect(user=pg_username, password=pg_password, database=pg_database)

print("Connection established")
#open cursor to perform data base operations
cursor = conn.cursor()
print("Cursor Working")
#execute command to create a new table
cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, first_name VARCHAR(50) NOT NULL,  last_name VARCHAR(50) NOT NULL, email VARCHAR(50) NOT NULL, gender STRING NOT NULL,  ip_address VARCHAR(50) NOT NULL, plant_specific STRING NOT NULL);"
               )
print("Cursor executed")
sql = "INSERT INTO test VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
print("inserted")
#cursor.executemany(sql, newlist)
try:
    cursor.executemany(sql, newlist)
except pg.ProgrammingError as err:
    print('cannot execute this line {}'.format(err))

#make the changes to the database persistent
conn.commit()

#close communication with the database
cursor.close()
conn.close()

