from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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

# Initialize the browser
def init_browser():
    # Choose the chromedriver path based on the operating system
    if os.name == 'nt':  # Windows system
        chrome_driver_path = 'C:/Users/Lychee/chromedriver-win64/chromedriver.exe'  # Replace with your Windows path
    else:  # Linux system (e.g., running in Docker)
        chrome_driver_path = '/usr/bin/chromedriver'

    # Set the chromedriver path and initialize the service
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service)
    return driver

# Generic function to load a page, wait for elements, and retrieve page content
def get_data(driver, postcode, tab_selector, content_id, cleaner_function):
    url = f"https://www.streetcheck.co.uk/postcode/{postcode}"
    driver.get(url)
    
    # Wait for the navigation bar to load
    wait_for_element(driver, By.ID, "postcodeTabs")
    
    # Click the specified tab button
    tab_button = driver.find_element(By.CSS_SELECTOR, tab_selector)
    driver.execute_script("arguments[0].click();", tab_button)
    
    # Wait for the content to load
    wait_for_element(driver, By.ID, content_id)
    
    # Parse the page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    content_section = soup.find("div", id=content_id)
    
    if content_section:
        content_text = content_section.get_text(separator='\n', strip=True)
        return cleaner_function(content_text)  # Call the passed cleaner function
    return f"No data found for {content_id}."

# Wait for an element to load
def wait_for_element(driver, by_type, identifier):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_type, identifier)))

# Get Summary data
def get_summary_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#summary"]', "summary", clean_summary_data)

# Get Housing data
def get_housing_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#housing"]', "housing", clean_housing_data)

# Get People data
def get_people_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#people"]', "people", clean_people_data)

# Get Culture data
def get_culture_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#culture"]', "culture", clean_culture_data)

# Get Employment data
def get_employment_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#employment"]', "employment", clean_employment_data)

# Get Crime data
def get_crime_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#policing"]', "policing", clean_crime_data)

# Get Nearby data
def get_nearby_data(driver, postcode):
    return get_data(driver, postcode, 'a[href="#nearby"]', "nearby", clean_nearby_data)
