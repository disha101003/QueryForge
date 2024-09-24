import requests
from bs4 import BeautifulSoup

# Define the URL for VLSI and Circuit Design faculty
url = "https://engineering.purdue.edu/ECE/People/Faculty/Areas/?area_id=2593"

# Fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the faculty members by locating the container with the people entries
faculty_list = soup.find_all('div', class_='people-list-details')

# Open a file to write the data
with open("vlsi_circuit_design_faculty.txt", "w") as file:
    # Iterate through the first 5 faculty members
    for faculty in faculty_list[:5]:
        # Extract professor name
       
        # Extract professor title (if available)
        title = faculty.find('div', class_='list-name').get_text(strip=True) if faculty.find('div', class_='person-title') else 'N/A'

        # Extract professor email (it may be in an 'a' tag with 'mailto:')
        email_tag = faculty.find('a', href=True)
        email = email_tag['href'].replace('mailto:', '') if email_tag and 'mailto:' in email_tag['href'] else 'N/A'

        # Extract contact number
        contact_number = faculty.find('div', class_='phone').get_text(strip=True) if faculty.find('div', class_='person-phone') else 'N/A'
        
        # Extract room number (if available)
        room_number = faculty.find('div', class_='person-office').get_text(strip=True) if faculty.find('div', class_='person-office') else 'N/A'

        # Write the details to the file
        file.write(f"Email: {email}\nContact Number: {contact_number}\nRoom Number: {room_number}\n\n")

print("Faculty data saved to 'vlsi_circuit_design_faculty.txt'")
