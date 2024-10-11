import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize browser and set browser masking
def init_browser():
    # Select chromedriver path based on the operating system
    if os.name == 'nt':  # Windows system
        chrome_driver_path = 'C:/Users/Lychee/chromedriver-win64/chromedriver.exe'  # Replace with your Windows path
    else:  # Linux system (e.g., when running in Docker)
        chrome_driver_path = '/usr/bin/chromedriver'

    # Create an instance of ChromeOptions
    chrome_options = Options()

    # Set the User-Agent in request headers to mimic a common browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    chrome_options.add_argument(f'user-agent={user_agent}')
    
    # Disable automation testing flag
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Hide automation browser flag
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # Set chromedriver path and initialize service
    service = Service(chrome_driver_path)
    
    # Launch the browser with specified options
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Disable WebDriver flag in the browser
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# Generic function to load the page, wait for an element, and retrieve page content
def get_raw_html(driver, postcode):
    url = f"https://www.streetcheck.co.uk/postcode/{postcode}"
    driver.get(url)

    try:
        wait_for_element(driver, By.ID, "postcodeTabs")  # Assume this element signifies page load completion
        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f"Error fetching data for {postcode}: {e}")
        return None

# Wait for an element to load
def wait_for_element(driver, by_type, identifier):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((by_type, identifier)))
    except Exception as e:
        print(f"Timeout waiting for element {identifier}: {e}")
        return False
    return True

# Extract all text content from the page and filter unnecessary data
def extract_all_text_from_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    all_text = soup.get_text(separator='\n', strip=True)

    # Filter out content starting from "Embed Codes & Links"
    cutoff_phrase = "Embed Codes & Links"
    cutoff_index = all_text.find(cutoff_phrase)
    if cutoff_index != -1:
        all_text = all_text[:cutoff_index]  # Truncate unnecessary content

    return all_text

# Retrieve raw data and extract text content
def get_all_data(postcode):
    driver = init_browser()  # Initialize the browser
    try:
        # Fetch page data
        raw_html = get_raw_html(driver, postcode)
        if raw_html:
            # Extract text information
            extracted_data = extract_all_text_from_html(raw_html)
            return extracted_data
        return None
    finally:
        driver.quit()
