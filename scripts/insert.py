import psycopg2 as ps2
import csv

# Assuming filename_list contains filenames, but you only open one file?
filename = 'MOCK_DATA-1.csv'
pg_username = 'postgres'
pg_password = '19019355'
pg_database = 'pre_ETL'

# Connect to database.
conn = ps2.connect(user=pg_username, password=pg_password, database=pg_database)
cursor = conn.cursor()

# Create table - execute only once or check if table exists before creating.
cursor.execute("CREATE TABLE IF NOT EXISTS test (id VARCHAR(50) PRIMARY KEY, first_name VARCHAR(50), last_name VARCHAR(50), email VARCHAR(50), gender VARCHAR(50), bitcoin_address VARCHAR(50), ethereum_address VARCHAR(50));")
print("Table ensured.")

# Prepare SQL for inserting data
sql = "INSERT INTO test (id, first_name, last_name, email, gender, bitcoin_address, ethereum_address) VALUES (%s, %s, %s, %s, %s, %s, %s)"

# Process CSV and batch insert into PostgreSQL
with open(f'../data/customer_mockdata.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    data_to_insert = [tuple(row) for row in reader]  # Ensure each row is a tuple

try:
    cursor.executemany(sql, data_to_insert)
    conn.commit()  # Commit changes
    print(f"Inserted {len(data_to_insert)} rows.")
except ps2.Error as e:
    print(f"Error inserting data: {e}")

# Clean up
cursor.close()
conn.close()
