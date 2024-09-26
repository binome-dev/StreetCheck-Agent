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

# Combine all data extraction into one main function
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
            print(f"Fetching {section} data...")
            all_data[section] = extractor(driver, postcode)
        
        return all_data

    finally:
        driver.quit()

# Test the combined function
if __name__ == "__main__":
    postcode = "E201GS"
    all_data = get_all_data(postcode)
    
    for section, data in all_data.items():
        print(f"--- {section} ---\n{data}\n")
