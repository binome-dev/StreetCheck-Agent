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

# Construct a list of postcode prefixes to filter (excluding prefixes with only letters)
postcode_prefixes = [
    'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9', 'E10', 'E11', 'E12', 'E13', 'E14', 'E15', 'E16', 'E17', 'E18', 'E1W', 'E20', 'E22', 'E98',
    'EC1A', 'EC1M', 'EC1N', 'EC1P', 'EC1R', 'EC1V', 'EC1Y', 'EC2A', 'EC2M', 'EC2N', 'EC2P', 'EC2R', 'EC2V', 'EC2Y', 'EC3A', 'EC3M', 'EC3N', 'EC3P',
    'EC3R', 'EC3V', 'EC4A', 'EC4M', 'EC4N', 'EC4P', 'EC4R', 'EC4V', 'EC4Y', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'N7', 'N8', 'N9', 'N10', 'N11', 'N12',
    'N13', 'N14', 'N15', 'N16', 'N17', 'N18', 'N19', 'N1C', 'N1P', 'N20', 'N21', 'N22', 'N81', 'NW1', 'NW2', 'NW3', 'NW4', 'NW5', 'NW6', 'NW7', 'NW8',
    'NW9', 'NW10', 'NW11', 'NW1W', 'NW26', 'SE1', 'SE2', 'SE3', 'SE4', 'SE5', 'SE6', 'SE7', 'SE8', 'SE9', 'SE10', 'SE11', 'SE12', 'SE13', 'SE14', 'SE15',
    'SE16', 'SE17', 'SE18', 'SE19', 'SE1P', 'SE20', 'SE21', 'SE22', 'SE23', 'SE24', 'SE25', 'SE26', 'SE27', 'SE28', 'SW2', 'SW3', 'SW4', 'SW5', 'SW6', 
    'SW7', 'SW8', 'SW9', 'SW10', 'SW11', 'SW12', 'SW13', 'SW14', 'SW15', 'SW16', 'SW17', 'SW18', 'SW19', 'SW1A', 'SW1E', 'SW1H', 'SW1P', 'SW1V', 'SW1W', 
    'SW1X', 'SW1Y', 'SW20', 'SW95', 'W2', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14', 'W1A', 'W1B', 'W1C', 'W1D', 'W1F', 
    'W1G', 'W1H', 'W1J', 'W1K', 'W1S', 'W1T', 'W1U', 'W1W', 'WC1A', 'WC1B', 'WC1E', 'WC1H', 'WC1N', 'WC1R', 'WC1V', 'WC1X', 'WC2A', 'WC2B', 'WC2E', 
    'WC2H', 'WC2N', 'WC2R', 'BR1', 'BR2', 'BR3', 'BR4', 'BR5', 'BR6', 'BR7', 'BR8', 'CR0', 'CR2', 'CR3', 'CR4', 'CR5', 'CR6', 'CR7', 'CR8', 'CR9', 'CR44', 
    'CR90', 'DA1', 'DA5', 'DA6', 'DA7', 'DA8', 'DA14', 'DA15', 'DA16', 'DA17', 'DA18', 'EN1', 'EN2', 'EN3', 'EN4', 'EN5', 'EN6', 'EN7', 'EN8', 'EN9', 'HA0',
    'HA1', 'HA2', 'HA3', 'HA4', 'HA5', 'HA6', 'HA7', 'HA8', 'HA9', 'IG1', 'IG2', 'IG3', 'IG4', 'IG5', 'IG6', 'IG7', 'IG8', 'IG9', 'IG11', 'KT1', 'KT2', 'KT3', 
    'KT4', 'KT5', 'KT6', 'KT7', 'KT8', 'KT9', 'KT17', 'KT18', 'KT19', 'KT22', 'RM1', 'RM2', 'RM3', 'RM4', 'RM5', 'RM6', 'RM7', 'RM8', 'RM9', 'RM10', 'RM11', 
    'RM12', 'RM13', 'RM14', 'RM15', 'SM1', 'SM2', 'SM3', 'SM4', 'SM5', 'SM6', 'SM7', 'TN14', 'TN16', 'TW1', 'TW2', 'TW3', 'TW4', 'TW5', 'TW6', 'TW7', 'TW8', 
    'TW9', 'TW10', 'TW11', 'TW12', 'TW13', 'TW14', 'TW15', 'TW19', 'UB1', 'UB2', 'UB3', 'UB4', 'UB5', 'UB6', 'UB7', 'UB8', 'UB9', 'UB10', 'UB11', 'UB18', 
    'WD3', 'WD6', 'WD23'
]

# Use str.startswith() to match postcode prefixes
london_postcodes = df_postcodes[df_postcodes['postcode'].str.startswith(tuple(postcode_prefixes))]['postcode']

# Extract the first 1000 postcodes
postcodes = london_postcodes[6800:200000]

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

# Batch insert data into the database
def insert_data_batch(cursor, batch_data):
    cursor.executemany('''INSERT INTO postcode_data 
                          (postcode, summary, housing, people, culture, employment, crime, nearby) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                          ON CONFLICT (postcode) DO NOTHING''', batch_data)

# Main function to extract all data for a given postcode
def get_all_data(postcode):
    driver = init_browser()  # Initialize the browser
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

# Batch fetch data and save it to PostgreSQL
def save_data_to_db(postcodes, cursor, conn, batch_size=10):
    batch_data = []
    for postcode in postcodes:
        # Check if the postcode already exists in the database
        if postcode_exists(cursor, postcode):
            print(f"Postcode {postcode} already exists in the database. Skipping...")
            continue

        # Get data corresponding to the postcode
        all_data = get_all_data(postcode)

        # Add the data to the batch list
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

        # Insert data and commit transactions when the batch size is reached
        if len(batch_data) >= batch_size:
            insert_data_batch(cursor, batch_data)
            conn.commit()  # Commit the transaction
            print(f"Committed a batch of {batch_size} records.")
            batch_data.clear()  # Clear the batch data

    # Insert any remaining data that hasn't been committed
    if batch_data:
        insert_data_batch(cursor, batch_data)
        conn.commit()
        print(f"Committed the remaining {len(batch_data)} records.")

if __name__ == "__main__":
    # Initialize the database connection
    conn, cursor = init_db()

    try:
        # Batch save data to the database, setting each batch to contain 10 records
        save_data_to_db(postcodes, cursor, conn, batch_size=10)
    finally:
        # Close the database connection
        conn.close()
