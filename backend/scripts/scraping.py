import urllib3
import bs4
import requests
from urllib import request
from bs4 import BeautifulSoup
import re


# def get_dict_courses(url):
#     response = requests.get(url)
#     courses_dict = {}
#     if response.status_code == 200:
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.text, 'html.parser')

#         # Extract data by navigating the HTML structure
#         links = soup.find_all('a')
#         for link in links:
#             if link.get('href').startswith('/courses'):
#                 #get names
#                 course_name = link.get_text(strip=True)
#                 course_name = re.sub(r'^ou', '', course_name) #some names have "ou" at the beginning - remove ou
#                 course_name = re.sub(r'\s*\([^)]*\)', '', course_name) #some names have () with details - remove (...)

#                 #get id
#                 href = link.get('href')
#                 course_id = href.split('/courses/')[-1]
#                 numbers = re.findall(r'\d+', course_id)[0] #some ids contain str - remove str

#                 #stock courses in dict
#                 courses_dict[course_name] = numbers
            
#     else:
#         print('Failed to retrieve the webpage')
    
#     return(courses_dict)


# #courses url
# url_1a = "https://www.ensae.fr/formation/cycle-ingenieur/premiere-annee-du-cycle-ingenieur"
# url_2a = "https://www.ensae.fr/formation/cycle-ingenieur/deuxieme-annee"
# url_3a = "https://www.ensae.fr/formation/cycle-ingenieur/troisieme-annee/catalogue-des-cours-de-troisieme-annee-du-cycle-ingenieur"

# courses_1a = get_dict_courses(url_1a)
# courses_2a = get_dict_courses(url_2a)
# courses_3a = get_dict_courses(url_3a)

# print(courses_1a)


# url = "https://pamplemousse.ensae.fr/index.php?p=40a"
# response = requests.get(url, verify=False)
# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.text)



# Ouvrir le fichier HTML
with open('../data/edt.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parser le contenu HTML avec BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the elements containing the relevant information
dates = soup.find_all('span', class_='fc-list-heading-main')
events = soup.find_all("tr", class_="fc-list-item")

# Initialize a list to store event data
event_data = []

# Iterate through the events and extract the information
for date in dates:
    day = date.text

    for event in events:
        time = event.find("td", class_="fc-list-item-time").get_text(strip=True)
        title = event.find("td", class_="fc-list-item-title").find("a")

        # Split the class title using a comma
        lesson_info = re.split(r',\s*', title.get_text())

        #Extract class info
        words_name = lesson_info[0].split()
        name = ' '.join(words_name[:-1]) # Join all words except the last one to get the name

        #Extract lesson info
        time_parts = time.split(" - ") # Extract day and start/end times from the time string
        start_time = time_parts[0]
        end_time = time_parts[1]
        lesson_type = re.search(r'(\w+)(?=\s*,\s*)', title.get_text()).group(1)
        teacher = lesson_info[-2]
        room = lesson_info[-1]
        event_info = (day, start_time, end_time, lesson_type, teacher, room)

        # Create an event dictionary
        event_dict = {
            "class_id": 1,
            "name": name,
            "ects": 1,
            # "room": "room",
            "lesson_info": [event_info],
            "backgroundColor": "#dbb1bc",
            # "teachers": "teachers",
            "link":"link",
        }

        event_data.append(event_dict)





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


## Combine lessons in one class
# Create a dictionary to store the combined entries
combined_data = {}

for entry in event_data:
    name = entry["name"]
    if name not in combined_data:
        combined_data[name] = entry
        combined_data[name]["lesson_info"] = [entry["lesson_info"]]
    else:
        combined_data[name]["lesson_info"].append(entry["lesson_info"])

# Convert the dictionary back to a list of JSON objects
result = list(combined_data.values())

# Print the result
import json
json_data = json.dumps(result, indent=4)
json_data = replace_unicode_escapes(json_data) # Replace Unicode escape sequences in the JSON data
print(json_data)

