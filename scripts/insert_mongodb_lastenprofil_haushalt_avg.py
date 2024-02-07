from pymongo import MongoClient
import csv
import sys

# Increase the maximum field size limit
max_int_c_long = 2**31 - 1  
csv.field_size_limit(max_int_c_long)

# MongoDB database and collection names
db_name = 'pre_ETL'
collection_name = 'bdew_lastenprofil_haushalt_avg'

# MongoDB connection string
mongo_uri = 'mongodb+srv://mongodb:19019355@etlpipeline.setotml.mongodb.net/'

# Connect to the MongoDB client
client = MongoClient(mongo_uri)

# Select the database and collection
db = client[db_name]
collection = db[collection_name]

filename = 'bdew_lastenprofil_haushalt_avg.csv'  # Adjust the filename as necessary

# Open the CSV file and read data
with open(f'../data/{filename}', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)  # Using DictReader to read the CSV into dictionaries
    documents = list(reader)  # Convert CSV data to a list of dictionaries

# Insert documents into MongoDB
try:
    # If you're inserting a lot of documents, consider using insert_many for efficiency.
    result = collection.insert_many(documents)
    print(f"Inserted {len(result.inserted_ids)} documents.")
except Exception as e:
    print(f"Error inserting documents: {e}")

# Close the MongoDB connection
client.close()