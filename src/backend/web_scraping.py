import requests
from bs4 import BeautifulSoup
import os

# URL of the professor's profile
url = "https://engineering.purdue.edu/ECE/People/ptProfile?resource_id=246563"

# Send a GET request to the URL
response = requests.get(url)


soup = BeautifulSoup(response.content, 'html.parser')
def find_next_info(label):
    element = soup.find(string=label)
    if element:
        return element.find_next().get_text(strip=True)
    else:
        print(f"Warning: '{label}' not found.")
        return "N/A"


name = soup.find('h1').get_text(strip=True)
office_element = soup.find(string="Office:")
if office_element:
   
    office = office_element.find_next(string=True).strip() 

    if "Phone:" in office:  
        office = office.split("Phone:")[0].strip() 
else:
    office = "N/A"
    print("Warning: 'Office:' not found.")

email = find_next_info('E-mail:')


research_heading = soup.find('h2', string='Research')
if research_heading:
    research_description = research_heading.find_next('p').get_text(strip=True)  
else:
    research_description = "N/A"
    print("Warning: 'Research' heading not found.")




print("Extracted Information:")
print(f"Name: {name}")
print(f"Office: {office}")
print(f"Email: {email}")
print(f"Research Description: {research_description}")


file_name = "professor_info_20.txt"
try:
    with open(file_name, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Office: {office}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Research Description: {research_description}\n")
except Exception as e:
    print(f"Error writing to file: {e}")

