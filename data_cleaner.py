import re

def clean_summary_data(raw_text):
    # Remove irrelevant links, prompts, and explanatory text
    raw_text = re.sub(r'(click here|view information|Save Postcode|Leaflet|Show Census Area Covered|View Fullscreen|Back to Top|Share|Tweet)', '', raw_text)
    
    # Remove unnecessary explanations
    raw_text = re.sub(r'(Please note:|This page|For information|Alternatively,|You can see|The figures|Continue Reading:|For more details).*', '', raw_text)

    # Define keywords to extract relevant information
    keywords = [
        r'(.*? is in .+?\. The postcode is within .+? ward/electoral division.*)',  # Match sentence describing location and electoral division
        r'Area Type\s*.+',  # Extract Area Type
        r'Local Authority\s*.+',  # Extract Local Authority information
        r'Ward\s*.+',  # Extract Ward information
        r'\bConstituency\b.*',  # Extract paragraphs or sentences with "Constituency"
        r'Region\s*.+',  # Match Region information (specific to England)
        r'Country\s*.+'  # Extract Country information
    ]
    
    # Keep only the matching sections
    relevant_sections = []
    for keyword in keywords:
        match = re.search(keyword, raw_text)
        if match:
            relevant_sections.append(match.group().strip())
    
    # Combine the matched sections into final text, cleaning up extra blank lines
    cleaned_text = "\n".join(relevant_sections)
    return cleaned_text

def clean_housing_data(raw_text):
    # Remove unnecessary links and irrelevant information
    raw_text = re.sub(r'(Embed This|Back to Top|View House Sale Prices|Are these numbers higher than you expected\? Click here for explanation.|the figures may include adjacent streets|see the Summary tab for an explanation and map of the area that these figures cover.)', '', raw_text)
    
    # Remove commentary inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)
    
    # Remove redundant paragraph descriptions
    raw_text = re.sub(r'(The area containing|This area contains|This contrasts with|Please note that)', '', raw_text)
    
    # Clean up blank lines and extra spaces
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_people_data(raw_text):
    # Remove descriptive text and irrelevant explanations
    raw_text = re.sub(r'(Embed This|Back\xa0to\xa0Top|Continue Reading:|Figures for relationship|Health in the UK|Education & Qualifications).*', '', raw_text)

    # Remove unnecessary descriptions like "Across the UK"
    raw_text = re.sub(r'Across the UK.*?\.', '', raw_text)

    # Clean irrelevant content inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)

    # Remove duplicate information and blank lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])

    return cleaned_text

def clean_culture_data(raw_text):
    # Remove specific irrelevant prompts and explanatory text
    raw_text = re.sub(r'(Embed This|Back\xa0to\xa0Top|Continue Reading:).*', '', raw_text)
    
    # Remove descriptive sentences and keep key information
    raw_text = re.sub(r'(As a country.*?|The largest.*?|Note that.*?|Figures for.*)', '', raw_text)
    
    # Clean up content inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)
    
    # Remove blank lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_employment_data(raw_text):
    # Remove extra descriptive sentences and prompts
    raw_text = re.sub(r'(Embed This|Back\xa0to\xa0Top|Continue Reading:|Figures for).*', '', raw_text)
    
    # Clean up content inside parentheses
    raw_text = re.sub(r'\(.*?\)', '', raw_text)

    # Remove specific paragraph descriptions
    raw_text = re.sub(r'(This address.*?|Figures for.*?|Classifications are.*)', '', raw_text)
    
    # Remove blank lines
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text

def clean_crime_data(raw_text):
    # Extract key information about police force and crime statistics
    location_info = re.search(r'.*?is within the.*?force area\.', raw_text, re.DOTALL)
    crime_info = re.search(r'In [A-Za-z]+\s\d{4},\s\d+\scrimes were reported within half a mile of [A-Za-z0-9\s]{5,7}', raw_text, re.DOTALL)
    
    # If a match is found, keep the relevant information
    cleaned_text = ''
    if location_info:
        cleaned_text += location_info.group(0).strip() + '\n'
    if crime_info:
        cleaned_text += crime_info.group(0).strip()

    return cleaned_text

import re

def clean_nearby_data(raw_text):
    # Remove irrelevant symbols, map prompts, and service descriptions, including "| © OpenStreetMap contributors"
    raw_text = re.sub(r'(\|?\s*©?\s*OpenStreetMap\s*contributors)', '', raw_text)
    
    # Remove other service prompts and unnecessary information
    raw_text = re.sub(r'(Below are the details of the closest services to .*|All distances are straightline distances.*|\* Distances are measured in a straight line.*)', '', raw_text)

    # Remove useless link prompts and symbols
    raw_text = re.sub(r'(interactive services map for .*|Leaflet|View .*|Railway\xa0Station|Hospital|GP|Primary\xa0School|Secondary\xa0School)', '', raw_text)

    # Clean up blank lines and keep the key information
    cleaned_text = "\n".join([line.strip() for line in raw_text.splitlines() if line.strip()])
    
    return cleaned_text
