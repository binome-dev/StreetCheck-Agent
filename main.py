import pandas as pd
import psycopg2
from scrapers import get_all_data

# Read CSV file containing UK postcodes
df_postcodes = pd.read_csv('Data/ukpostcodes.csv')

# Build a list of postcode prefixes to filter by (excluding those with only letters)
postcode_prefixes = [
    "E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E20", "E22", "E98",
    "EC1A", "EC1M", "EC1N", "EC1P", "EC1R", "EC1V", "EC1Y", "EC2A", "EC2M", "EC2N", "EC2P", "EC2R", "EC2V", "EC2Y", "EC3A", "EC3M", "EC3N", "EC3P", "EC3R", "EC3V", "EC4A", "EC4M", "EC4N", "EC4P", "EC4R", "EC4V", "EC4Y",
    "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10", "N11", "N12", "N13", "N14", "N15", "N16", "N17", "N18", "N19", "N1C", "N1P", "N20", "N21", "N22", "N81",
    "NW1", "NW2", "NW3", "NW4", "NW5", "NW6", "NW7", "NW8", "NW9", "NW10", "NW11", "NW26",
    "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE7", "SE8", "SE9", "SE10", "SE11", "SE12", "SE13", "SE14", "SE15", "SE16", "SE17", "SE18", "SE19", "SE1P", "SE20", "SE21", "SE22", "SE23", "SE24", "SE25", "SE26", "SE27", "SE28",
    "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8", "SW9", "SW10", "SW11", "SW12", "SW13", "SW14", "SW15", "SW16", "SW17", "SW18", "SW19", "SW1A", "SW1E", "SW1H", "SW1P", "SW1V", "SW1W", "SW1X", "SW1Y", "SW20", "SW95",
    "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13", "W14", "W1A", "W1B", "W1C", "W1D", "W1F", "W1G", "W1H", "W1J", "W1K", "W1S", "W1T", "W1U", "W1W",
    "WC1A", "WC1B", "WC1E", "WC1H", "WC1N", "WC1R", "WC1V", "WC1X", "WC2A", "WC2B", "WC2E", "WC2H", "WC2N", "WC2R"
]

# Match postcode prefixes using str.startswith()
london_postcodes = df_postcodes[df_postcodes['postcode'].str.startswith(tuple(postcode_prefixes))]['postcode']

# Extract the first 2,000,000 postcodes
postcodes = london_postcodes[:2000000]

# Initialize database connection
def init_db():
    conn = psycopg2.connect(
        dbname="StreetCheck", 
        user="postgres", 
        password="Ephemeral", 
        host="localhost", 
        port="9999"
    )
    cursor = conn.cursor()
    return conn, cursor

# Check if postcode already exists in the database
def postcode_exists(cursor, postcode):
    cursor.execute('SELECT 1 FROM postcode_data WHERE postcode = %s', (postcode,))
    return cursor.fetchone() is not None

# Batch insert data into the database
def insert_data_batch(cursor, batch_data):
    cursor.executemany('''
        INSERT INTO postcode_data (postcode, information)
        VALUES (%s, %s)
        ON CONFLICT (postcode) DO NOTHING;
    ''', batch_data)

# Batch fetch data and save to PostgreSQL database
def save_data_to_db(postcodes, cursor, conn, batch_size=10):
    batch_data = []  # Store batch data
    for postcode in postcodes:
        # Check if the postcode already exists in the database
        if postcode_exists(cursor, postcode):
            print(f"Postcode {postcode} already exists in the database. Skipping...")
            continue

        # Fetch data for the postcode
        information = get_all_data(postcode)
        
        if information:
            batch_data.append((postcode, information))
            print(f"Fetched data for postcode {postcode}.")

        # Insert data when batch size is reached
        if len(batch_data) >= batch_size:
            insert_data_batch(cursor, batch_data)
            conn.commit()  # Commit transaction
            print(f"Inserted a batch of {batch_size} records.")
            batch_data.clear()  # Clear batch data

    # Insert any remaining data not yet committed
    if batch_data:
        insert_data_batch(cursor, batch_data)
        conn.commit()
        print(f"Inserted the remaining {len(batch_data)} records.")

if __name__ == "__main__":
    # Initialize database connection
    conn, cursor = init_db()

    try:
        # Save data to the database, 10 records per batch
        save_data_to_db(postcodes, cursor, conn, batch_size=10)
    finally:
        # Close the database connection
        conn.close()
