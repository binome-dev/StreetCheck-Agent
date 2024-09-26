import re

def clean_summary_data(raw_text):
    # Remove links and descriptive text
    raw_text = re.sub(r'(click here|view information|Save Postcode|Leaflet|Show Census Area Covered|View Fullscreen|Back to Top)', '', raw_text)
    
    # Remove "Please note" and other redundant descriptions
    raw_text = re.sub(r'(Please note:|This page|For information|Alternatively,|You can see|The figures|Continue Reading:).*', '', raw_text)

    # Remove irrelevant information inside parentheses, such as (e.g.)
    raw_text = re.sub(r'\(.*?\)', '', raw_text)
    
    # Clean up empty lines and extra spaces
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_housing_data(raw_text):
    # Remove unnecessary links and irrelevant information
    raw_text = re.sub(r'(Embed This|Back to Top|View House Sale Prices)', '', raw_text)
    
    # Remove commentary inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)
    
    # Remove redundant paragraph descriptions
    raw_text = re.sub(r'(The area containing|This area contains|This contrasts with|Please note that)', '', raw_text)
    
    # Clean up empty lines and extra spaces
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_people_data(raw_text):
    # Remove descriptive text and irrelevant notes
    raw_text = re.sub(r'(Embed This|Back to Top|Continue Reading:|Figures for relationship|Health in the UK|Education & Qualifications).*', '', raw_text)

    # Remove irrelevant notes containing phrases like "Across the UK"
    raw_text = re.sub(r'Across the UK.*?\.', '', raw_text)

    # Clean up irrelevant information inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)

    # Remove duplicate information and empty lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])

    return cleaned_text

def clean_culture_data(raw_text):
    # Remove specific useless prompts and descriptive text
    raw_text = re.sub(r'(Embed This|Back to Top|Continue Reading:|International Way).*', '', raw_text)
    
    # Remove descriptive sentences, keep key information
    raw_text = re.sub(r'(As a country.*?|The largest.*?|Note that.*?|Figures for.*)', '', raw_text)
    
    # Clean up content inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)
    
    # Remove empty lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_employment_data(raw_text):
    # Remove redundant descriptive sentences and prompts
    raw_text = re.sub(r'(Embed This|Back to Top|Continue Reading:|Figures for).*', '', raw_text)
    
    # Clean up content inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)

    # Remove specific paragraph descriptions
    raw_text = re.sub(r'(This address.*?|Figures for.*?|Classifications are.*)', '', raw_text)
    
    # Remove empty lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_crime_data(raw_text):
    # Extract key information about police forces and crime statistics
    location_info = re.search(r'.*?is within the.*?force area\.', raw_text, re.DOTALL)
    crime_info = re.search(r'In [A-Za-z]+\s\d{4},\s\d+\scrimes were reported within half a mile of [A-Za-z0-9\s]{5,7}', raw_text, re.DOTALL)
    
    # If matches are found, keep the relevant information
    cleaned_text = ''
    if location_info:
        cleaned_text += location_info.group(0).strip() + '\n'
    if crime_info:
        cleaned_text += crime_info.group(0).strip()

    return cleaned_text

def clean_nearby_data(raw_text):
    # Remove map and service prompts
    raw_text = re.sub(r'(\+|−|Leaflet|\|© OpenStreetMap contributors|interactive services map.*)', '', raw_text)
    
    # Remove useless link prompts
    raw_text = re.sub(r'View .*', '', raw_text)

    # Clean up empty lines, keeping key information
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text
