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


