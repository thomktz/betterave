import urllib3
import bs4
import requests
from urllib import request
from bs4 import BeautifulSoup
import re


#Get some info of classes from ensae.fr
def get_dict_courses(url):
    response = requests.get(url)
    courses_dict = {}
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract data by navigating the HTML structure
        links = soup.find_all('a')
        for link in links:
            if link.get('href').startswith('/courses'):
                #get names
                course_name = link.get_text(strip=True)
                course_name = re.sub(r'^ou', '', course_name) #some names have "ou" at the beginning - remove ou
                course_name = re.sub(r'\s*\([^)]*\)', '', course_name) #some names have () with details - remove (...)

                #get id
                href = link.get('href')
                course_id = href.split('/courses/')[-1]
                numbers = re.findall(r'\d+', course_id)[0] #some ids contain str - remove str

                #stock courses in dict
                courses_dict[course_name] = numbers
            
    else:
        print('Failed to retrieve the webpage')
    
    return(courses_dict)


#courses url
url_1a = "https://www.ensae.fr/formation/cycle-ingenieur/premiere-annee-du-cycle-ingenieur"
url_2a = "https://www.ensae.fr/formation/cycle-ingenieur/deuxieme-annee"
url_3a = "https://www.ensae.fr/formation/cycle-ingenieur/troisieme-annee/catalogue-des-cours-de-troisieme-annee-du-cycle-ingenieur"

courses_1a = get_dict_courses(url_1a)
courses_2a = get_dict_courses(url_2a)
courses_3a = get_dict_courses(url_3a)

courses_ensae_dict = {key: value for d in (courses_1a, courses_2a, courses_3a) for key, value in d.items()}




# Ouvrir le fichier HTML
with open('../data/edt.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')


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


# # Print the events for each date
# for date, event_list in date_events.items():
#     print(f"Date: {date}")
#     for event in event_list:
#         print(f"Event: {event}")



# Initialize a list to store event data
event_data = []

for date, event_list in date_events.items():
    # print(f"Date: {date}")
    # Iterate through the events and extract the information
    for event in event_list:

        time = event.find("td", class_="fc-list-item-time").get_text(strip=True)
        title = event.find("td", class_="fc-list-item-title").find("a")

        # Split the class title using a comma
        lesson_info = re.split(r',\s*', title.get_text())

        #Extract class info
        # words_name = lesson_info[0].split()
        # name = ' '.join(words_name[:-1]) # Join all words except the last one to get the name
        name = lesson_info[0].split(" (", 1)[0]

        #Extract lesson info
        time_parts = time.split(" - ") # Extract day and start/end times from the time string
        start_time = time_parts[0]
        end_time = time_parts[1]

        lesson_type = lesson_info[0].split()[-1]
        if not(lesson_type.startswith('Cours')) and not(lesson_type.startswith('TP')) and not(lesson_type.startswith('TD')):
            lesson_type = "TBD"
        
        if lesson_info[-2].isupper():
            teacher = lesson_info[-2]
        else:
            teacher = "TBD"

        room = lesson_info[-1]
        event_info = (date, start_time, end_time, lesson_type, teacher, room)

        background_color = event.find('span', class_='fc-event-dot')['style'].split(':')[1]


        # Create an event dictionary
        event_dict = {
            "class_id": "TBD",
            "name": name,
            "ects": "TBD",
            "lesson_info": [event_info],
            "backgroundColor": background_color,
            "link":"link",
        }

        event_data.append(event_dict)



## Combine lessons in one class
# Create a dictionary to store the combined entries
combined_data = {}

for entry in event_data:
    name = entry["name"]
    if name not in combined_data:
        combined_data[name] = entry
        combined_data[name]["lesson_info"] = entry["lesson_info"]
    else:
        combined_data[name]["lesson_info"].append(entry["lesson_info"][0])

# Convert the dictionary back to a list of JSON objects
result = list(combined_data.values())




# Match classes for class_id, ects and link with scraping from ensae.fr
for entry in result:
    for class_name, class_id in courses_ensae_dict.items():
        if (entry["name"]==class_name) :
        # if (entry["name"].startswith(class_name)) or (class_name.startswith(entry["name"])) :
            # print(entry["name"])
            entry["class_id"] = class_id
            link_class = "https://www.ensae.fr/courses/" + class_id
            entry["link"] = link_class

            # #Get ECTS
            ects_soup = BeautifulSoup(requests.get(link_class).text, 'html.parser')
            ects_element = ects_soup.find('b', string='Crédits ECTS :')
            if ects_element:
                ects_value = ects_element.find_next('br').next_sibling.strip()
                entry["ects"] = ects_value
                # print("ECTS Value:", ects_value)
            else:
                print("ECTS information not found.")



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


# Print the result
import json
json_data = json.dumps(result, indent=4)
json_data = replace_unicode_escapes(json_data) # Replace Unicode escape sequences in the JSON data
print(json_data)


# # Specify the file path where you want to save the JSON data
# file_path = "edt.json"
# # Save the JSON data to the file
# with open(file_path, 'w') as json_file:
#     json.dump(json_data, json_file)