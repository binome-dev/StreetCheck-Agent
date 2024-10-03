import pandas as pd
import psycopg2
from scrapers import (
    get_summary_data,
    get_housing_data,
    get_people_data,
    get_culture_data,
    get_employment_data,
    get_crime_data,
    get_nearby_data,
    init_browser
)

# Read the CSV file containing UK postcodes
df_postcodes = pd.read_csv('Data/ukpostcodes.csv')

# Extract the first 1000 postcodes
postcodes = df_postcodes['postcode'][:1000]

# Initialize the database connection
def init_db():
    conn = psycopg2.connect(
        dbname="postcode_db", 
        user="postgres", 
        password="Ephemeral", 
        host="localhost", 
        port="9999"
    )
    cursor = conn.cursor()
    return conn, cursor

# Check if the postcode already exists in the database
def postcode_exists(cursor, postcode):
    cursor.execute('SELECT 1 FROM postcode_data WHERE postcode = %s', (postcode,))
    return cursor.fetchone() is not None

# Insert a batch of data into the database
def insert_data_batch(cursor, batch_data):
    cursor.executemany('''INSERT INTO postcode_data 
                          (postcode, summary, housing, people, culture, employment, crime, nearby) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                          ON CONFLICT (postcode) DO NOTHING''', batch_data)

# Extract all data for a given postcode
def get_all_data(postcode):
    driver = init_browser()  # Initialize browser
    try:
        data_extractors = {
            "Summary": get_summary_data,
            "Housing": get_housing_data,
            "People": get_people_data,
            "Culture": get_culture_data,
            "Employment": get_employment_data,
            "Crime": get_crime_data,
            "Nearby": get_nearby_data
        }
        
        all_data = {}
        for section, extractor in data_extractors.items():
            print(f"Fetching {section} data for {postcode}...")
            all_data[section] = extractor(driver, postcode)
        
        return all_data

    finally:
        driver.quit()

# Fetch data in batches and save to PostgreSQL database
def save_data_to_db(postcodes, cursor, conn, batch_size=10):
    batch_data = []
    for postcode in postcodes:
        # Check if postcode already exists in the database
        if postcode_exists(cursor, postcode):
            print(f"Postcode {postcode} already exists in the database. Skipping...")
            continue

        # Fetch data for the postcode
        all_data = get_all_data(postcode)

        # Add data to the batch list
        batch_data.append((
            postcode, 
            all_data.get("Summary", 'N/A'),
            all_data.get("Housing", 'N/A'),
            all_data.get("People", 'N/A'),
            all_data.get("Culture", 'N/A'),
            all_data.get("Employment", 'N/A'),
            all_data.get("Crime", 'N/A'),
            all_data.get("Nearby", 'N/A')
        ))

        # Insert data and commit the transaction when batch size is reached
        if len(batch_data) >= batch_size:
            insert_data_batch(cursor, batch_data)
            conn.commit()  # Commit the transaction
            print(f"Committed a batch of {batch_size} records.")
            batch_data.clear()  # Clear the batch data

    # Insert any remaining uncommitted data
    if batch_data:
        insert_data_batch(cursor, batch_data)
        conn.commit()
        print(f"Committed the remaining {len(batch_data)} records.")

if __name__ == "__main__":
    # Initialize the database connection
    conn, cursor = init_db()

    try:
        # Save data in batches to the database, batch size of 10
        save_data_to_db(postcodes, cursor, conn, batch_size=10)
    finally:
        # Close the database connection
        conn.close()
