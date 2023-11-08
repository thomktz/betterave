import requests
from urllib import request
from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
import random


# Courses url
URL_1A = "https://www.ensae.fr/formation/cycle-ingenieur/premiere-annee-du-cycle-ingenieur"
URL_2A = "https://www.ensae.fr/formation/cycle-ingenieur/deuxieme-annee"
URL_3A = "https://www.ensae.fr/formation/cycle-ingenieur/troisieme-annee/catalogue-des-cours-de-troisieme-annee-du-cycle-ingenieur"

# Data paths
PATH_OCTOBER = 'data/edt_october.html'
PATH_NOV = 'data/edt_november.html'
PATH_DEC = 'data/edt_december.html'


# Classes names that need to be mapped
MAPPING = {"Sport - S1": "Sport",
           "Introduction à l'informatique - 1A-Eco":"Introduction à l’informatique",
            "Algorithmes et programmation":"Algorithmes et programmation / Python",
            "Bases de données":"Introduction aux bases de données", 
            "Estimation non paramétrique ":"Estimation non paramétrique", 
            "Theory of Industrial Organization ":"Theory of Industrial Organization", 
            # "Anglais 2A - S1":"Anglais", 
            # "Instruments Financiers 3A":"Financial instruments",
            "Théorie des probabilités - 2AD": "Théorie des probabilités", 
            # "Anglais 1A - S1":"Anglais", 
            "Experiments in Economics and Social Sciences ":"Experiments in Economics and Social Sciences",
            "Financial Econometrics ":"Financial Econometrics", 
            "Blockchain: Bitcoin and Smart-Contracts ":"Blockchain: Bitcoin and Smart-Contracts", 
            "Catastrophic Risks":"Catastrophic Risks, Cyber Risk and Insurance Markets", 
            "Python pour la data-science ": "Python pour la data science",
            # "Financial Instruments 2A":"Financial instruments", 
            "Macroeconometrics: Advanced Time-Series Analysis ": "Macroeconometrics: Advanced Time-Series Analysis",
            "Économétrie 1":"Econométrie 1",
            "Séminaire d'économie":"Séminaire d’économie",
            "Ethics and responsibility in data science":"Ethics and responsibility in data science- group 1",
            "Ethics and responsibility in data science- group 2 ":"Ethics and responsibility in data science- group 2",
            "Machine learning for Portfolio Management and Trading ":"Machine learning for Portfolio Management and Trading"
            }

# Classes in calendar that are either not classes, either not for 1a, 2a, 3a
CLASSES_TO_REMOVE = ['Réservation salles ENSAE','Blocage salles soutenances','Projet data science et sciences sociales - S1',
                     "Théorie microéconomique appliquée  à l'assurance", 'Introduction to time series econometrics',
                     'Mathématiques et apprentissage statistique pour économistes MS', 'Energy Transition M1MIE – X', 
                     'Advanced Microeconomics: game theory and applications', 'Suivi des mémoires SQD ',
                     'Introduction à la finance mathématique - MS', 'Econométrie 3A-CI/MS', 'Information and Expectations in Macroeconomics ',
                     'Microéconomie 3A-CI/MS', 'Risk Theory - 3A/MS/M2', "Initiation à l'économie", 'Réservation salles X',
                     'Statistique mathématique - CI/SFA', 'Statistique mathématique - MS','Statistical learning theory',
                     'Asset Pricing: Theoretical Foundations', 'Macroéconomie 3A-CI/MS', 'Introduction à l’apprentissage statistique - CI/MS', 
                     'Dynamic optimization and reinforcement learning', 'Time Series  3A-CI/MS', 'Financial time series ', 
                     'Banking and Financial Intermediation', 'Corporate Finance Theory', "Machine Learning avec Python",
                     'Compétences professionnelles 2 : L’entretien de recrutement', 'Natural Language processing from pre-neural to transformers',
                     'Conférences professionnelles Economic Policies and Dynamics', 'Evolutionary Game Theory',
                     "Stochastic Calculus - Long course - SFA"
                     ]

# Remove classes that are in fact special events
EVENTS_TO_REMOVE = ["Conférences d'introduction aux enjeux sociaux contemporains",
                    'Forum ENSAE - Conférence Insee',
                    "Atelier préparation stage d'application",
                    'Amphi de présentation relations internationales', 
                    'Amphi de présentation stage 1A',
                    'Forum Trium', 
                    'Présentation relations internationales',
                    'Méthodes pour la rédaction d’une candidature',
                    'Forum ASTER',
                    'Business Data Challenge'
                    ]


def get_dict_courses(url, level):
    """Get class_ids and classes' names from ensae.fr

    Args:
        url (str): url for scraping
        level (str) : level of classes scraped
    """
    response = requests.get(url)
    courses_dict = {}

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser') # Parse the HTML content of the page
        links = soup.find_all('a') # Extract data by navigating the HTML structure

        for link in links:
            if link.get('href').startswith('/courses'):
                #get names
                course_name = link.get_text(strip=True)
                course_name = re.sub(r'^ou', '', course_name) #some names have "ou" at the beginning - remove "ou"
                course_name = re.sub(r'\s*\([^)]*\)', '', course_name) #some names have () with details - remove (...)

                #get id
                href = link.get('href')
                course_id = href.split('/courses/')[-1]
                numbers = re.findall(r'\d+', course_id)[0] #some ids contain str - remove str

                #stock courses in dict
                courses_dict[course_name] = [numbers, level]

    else:
        print('Failed to retrieve the webpage')
    
    return(courses_dict)


def transform_date_french_to_iso(date_french):
    # Split the date string into its components
    day, month, year = date_french.split()
    
    # Define a mapping of French month names to month numbers
    month_mapping = {
        "janvier": "01",
        "février": "02",
        "mars": "03",
        "avril": "04",
        "mai": "05",
        "juin": "06",
        "juillet": "07",
        "août": "08",
        "septembre": "09",
        "octobre": "10",
        "novembre": "11",
        "décembre": "12"
    }

    # Format the date components in the desired format
    formatted_date = f"{year}-{month_mapping[month.lower()]}-{day.zfill(2)}"

    return formatted_date


def transform_time(original_time):
    try:
        # Parse the original time using the original format
        original_datetime = datetime.strptime(original_time, '%H:%M')

        # Format the time to match the new format '%H:%M:%S'
        new_time_format = original_datetime.strftime('%H:%M:%S')

        return new_time_format
    except ValueError:
        # Handle the case where the input time format is invalid
        raise ValueError("Invalid input type format")


def scrap_events_data(path):
    """Scrap classes schedule

    Args:
        path (str): classes schedule as an html.
    """
    with open(path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser') # Parser le contenu HTML avec BeautifulSoup

    # Find the elements containing the relevant information
    dates = soup.find_all('span', class_='fc-list-heading-main')
    events = soup.find_all("tr", class_="fc-list-item")

    # Create a dictionary to store events for each date
    date_events = {}
    current_date = None  # Initialize the current date to None

    # Iterate through dates and extract events
    for i in range(len(events)):
        if dates and events[i].find_previous('span', class_='fc-list-heading-main') == dates[0]:
            current_date = dates.pop(0).text  # Get the text of the date

        if current_date is not None:
            event_name = events[i]  # Get the html of the event
            date_events.setdefault(current_date, []).append(event_name)

    # Initialize a list to store event data
    event_data = []

    for date, event_list in date_events.items():
        for event in event_list: # Iterate through the events and extract the information
            time = event.find("td", class_="fc-list-item-time").get_text(strip=True)
            title = event.find("td", class_="fc-list-item-title").find("a")

            lesson_info = re.split(r',\s*', title.get_text()) # Split the class title using a comma
            name = lesson_info[0].split(" (", 1)[0] #Extract class info

            #Extract lesson info
            time_parts = time.split(" - ") # Extract day and start/end times from the time string
            start_time = time_parts[0]
            end_time = time_parts[1]

            lesson_type = lesson_info[0].split()[-1]

            if lesson_info[-2].isupper():
                prenom = "Prof"
                teacher = [prenom, lesson_info[-2].capitalize()]
            else:
                teacher = ["Prof", "Martin"]

            room = lesson_info[-1]
            date_iso = transform_date_french_to_iso(date)
            event_info = (date_iso, transform_time(start_time), transform_time(end_time), lesson_type, teacher, room)

            background_color = event.find('span', class_='fc-event-dot')['style'].split(':')[1]

            # Create an event dictionary
            event_dict = {
                "class_id": "TBD",
                "name": name,
                "ects": "TBD",
                "lesson_info": [event_info],
                "backgroundColor": background_color,
                "teacher_name":"TBD",
                "level":"TBD"
            }

            # Assign first teacher to global teacher for now
            event_dict["teacher_name"] = event_info[4]

            event_data.append(event_dict)

    return(event_data)


def combine_lessons(event_data):
    """Combine lessons info within a class

    Args:
        event_data (list of dict): list of dict with entries by classes
    """
    combined_data = {} # Create a dictionary to store the combined entries

    for entry in event_data:
        name = entry["name"]
        if name not in combined_data:
            combined_data[name] = entry
            combined_data[name]["lesson_info"] = entry["lesson_info"]
        else:
            combined_data[name]["lesson_info"].append(entry["lesson_info"][0])

    result = list(combined_data.values()) # Convert the dictionary back to a list of JSON objects
    return result


def match_id_ects(event_data, MAPPING=MAPPING):
    """Match id and ects to a class

    Args:
        event_data (list of dict): list of dict with entries by classes
    """
    classes_unclassified = []
    courses_ensae_dict = {key: value for d in (get_dict_courses(URL_1A, "1A"), get_dict_courses(URL_2A, "2A"), get_dict_courses(URL_3A, "3A")) for key, value in d.items()}

    # Match classes for class_id, ects and link with scraping from ensae.fr
    for entry in event_data:
        if (entry["name"] in MAPPING): #if different name, we match both
            new_name = entry["name"]
            entry["name"] = MAPPING[new_name]
        
        # Exceptions
        if entry["name"]=="Anglais 2A - S1":
            entry["class_id"]=5797
            entry["ects"]=2.0
            entry["level"]="2A"
        if entry["name"]=="Anglais 1A - S1":
            entry["class_id"]=5792
            entry["ects"]=2.0
            entry["level"]="1A"
        if entry["name"]=="Instruments Financiers 3A":
            entry["class_id"]=1088
            entry["ects"]=0.0
            entry["level"]="3A"
        if entry["name"]=="Financial Instruments 2A":
            entry["class_id"]=71
            entry["ects"]=2.5
            entry["level"]="2A"
        
        for class_name, class_id_level in courses_ensae_dict.items():
            class_id = class_id_level[0]
            level = class_id_level[1]

            if (entry["name"].lower() == class_name.lower()):
                link_class = "https://www.ensae.fr/courses/" + class_id
                entry["class_id"] = int(class_id)
                # entry["link"] = link_class

                #Get level
                entry["level"] = level

                #Get ECTS
                ensae_soup = BeautifulSoup(requests.get(link_class).text, 'html.parser')

                ects_element = ensae_soup.find('b', string='Crédits ECTS :')
                if ects_element:
                    ects_value = ects_element.find_next('br').next_sibling.strip()
                    entry["ects"] = float(ects_value)
                else:
                    print("ECTS information not found.")

                teacher_element = ensae_soup.find('h4', string='Enseignant')
                if teacher_element:
                    teacher_element_2 = teacher_element.find_next('a')
                    if teacher_element_2:
                        teacher_value = teacher_element_2.find_next('a').text
                        entry["teacher_name"] = teacher_value.strip().split()
                        entry["teacher_name"][0] = entry["teacher_name"][0].capitalize()
                        entry["teacher_name"] = entry["teacher_name"][::-1]

        if entry["class_id"]=="TBD":
            classes_unclassified.append(entry["name"])

        # Exceptions bc of len(name)
        if entry["teacher_name"]==['David', 'Olivier', 'Zerbib']:
            entry["teacher_name"]=['Olivier', 'Zerbib']
            
    return(event_data, classes_unclassified)


def replace_unicode_escapes(obj):
    """
    Replace unicode escapes in json, for instance replace \u00e9 by é
    """
    if isinstance(obj, str):
        return obj.encode('utf-8').decode('unicode_escape')
    elif isinstance(obj, list):
        return [replace_unicode_escapes(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: replace_unicode_escapes(value) for key, value in obj.items()}
    return obj


if __name__ == "__main__":
    # Scrap data
    event_data_oct = scrap_events_data(PATH_OCTOBER)
    event_data_nov = scrap_events_data(PATH_NOV)
    event_data_dec = scrap_events_data(PATH_DEC)

    # Concatenate html
    event_data = event_data_oct + event_data_nov + event_data_dec
    event_data_by_classes = combine_lessons(event_data)
        
    # Create a special events json
    special_events = [item for item in event_data_by_classes if item['name'] in EVENTS_TO_REMOVE]

    # Remove useless classes from event_data
    event_data_by_classes_filtered = [item for item in event_data_by_classes if item['name'] not in CLASSES_TO_REMOVE]
    event_data_by_classes_filtered = [item for item in event_data_by_classes_filtered if item['name'] not in EVENTS_TO_REMOVE]

    # Get result
    final_classes_data, classes_unclassified = match_id_ects(event_data_by_classes_filtered)
    # print(classes_unclassified)

    # Save result
    json_data = json.dumps(final_classes_data, indent=4)
    json_data = replace_unicode_escapes(json_data) # Replace Unicode escape sequences in the JSON data
    file_name = "classes.json"
    with open("data/" + file_name, 'w') as json_file:
        json_file.write(json_data)
    
    json_data_special_events = json.dumps(special_events, indent=4)
    json_data_special_events = replace_unicode_escapes(json_data_special_events)
    file_name_2 = "special_events.json"
    with open("data/" + file_name_2, 'w') as json_file:
        json_file.write(json_data_special_events)

