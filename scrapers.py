from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
from data_cleaner import (
    clean_summary_data, clean_housing_data, clean_people_data,
    clean_culture_data, clean_employment_data, clean_crime_data,
    clean_nearby_data
)

# Initialize the browser and set request headers for user-agent masking
def init_browser():
    # Choose the path for chromedriver based on the operating system
    if os.name == 'nt':  # Windows system
        chrome_driver_path = 'C:/Users/Lychee/chromedriver-win64/chromedriver.exe'  # Replace with your Windows path
    else:  # Linux system (e.g., running in Docker)
        chrome_driver_path = '/usr/bin/chromedriver'

    # Create an instance of ChromeOptions
    chrome_options = Options()

    # Set the request header's User-Agent to mimic a common browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')

    # Set the chromedriver path and initialize the service
    service = Service(chrome_driver_path)
    
    # Launch the browser with the specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

# A general function to load the page, wait for elements, and retrieve content
def get_data(driver, postcode, tab_selector, content_id, cleaner_function, default_message="No data available"):
    url = f"https://www.streetcheck.co.uk/postcode/{postcode}"
    driver.get(url)
    
    # Try loading the page content and handle exceptions
    try:
        # Wait for the navigation bar to load
        wait_for_element(driver, By.ID, "postcodeTabs")
        
        # Attempt to click the specified tab button
        tab_button = driver.find_element(By.CSS_SELECTOR, tab_selector)
        driver.execute_script("arguments[0].click();", tab_button)
        
        # Wait for the content to finish loading
        wait_for_element(driver, By.ID, content_id)
        
        # Parse the page
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content_section = soup.find("div", id=content_id)
        
        if content_section:
            content_text = content_section.get_text(separator='\n', strip=True)
            return cleaner_function(content_text)  # Call the provided cleaning function
        return default_message
    except Exception as e:
        print(f"Error fetching {content_id} data for {postcode}: {e}")
        return default_message

# Wait for elements to load
def wait_for_element(driver, by_type, identifier):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_type, identifier)))
    except Exception as e:
        print(f"Timeout waiting for element {identifier}: {e}")
        return False
    return True

# Fetch Summary data
def get_summary_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#summary"]', "summary", clean_summary_data, "No summary data available")

# Fetch Housing data
def get_housing_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#housing"]', "housing", clean_housing_data, "No housing data available")

# Fetch People data
def get_people_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#people"]', "people", clean_people_data, "No people data available")

# Fetch Culture data
def get_culture_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#culture"]', "culture", clean_culture_data, "No culture data available")

# Fetch Employment data
def get_employment_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#employment"]', "employment", clean_employment_data, "No employment data available")

# Fetch Crime data
def get_crime_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#policing"]', "policing", clean_crime_data, "No crime data available")

# Fetch Nearby data
def get_nearby_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#nearby"]', "nearby", clean_nearby_data, "No nearby data available")
