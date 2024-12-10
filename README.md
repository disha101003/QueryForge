## QueryForge
This web application aims to streamline the process of discovering research opportunities within a university setting. By aggregating data on professors, research projects, and student positions from multiple sources, this tool allows students to search for research projects relevant to their interests. 

As students, we understand the challenge of finding research opportunities due to scattered information. This tool provides a centralized database with enhanced search and filtering functionalities, tailored to support students in the ECE department, with plans to expand to additional departments.

## Team Members

* Stuti Rastogi
* Disha Maheshwari


## Accessing the Application
1. **Open the Web Application**: Go to the application URL (http://3.142.98.164:5000/) in your preferred web browser.
2. **Login**: Sign in using your credentials. If you are new to the application, you will be asked to create an account.

## Features and Usage

### Features
- **Research Opportunity Aggregation**: Gathers data on professors, research projects, and student openings across the ECE department.
- **Resume Parser**: Enables users to upload their resumes, extract key skills and qualifications, and match them with relevant research projects.
- **Advanced Search**: Allows users to search and filter opportunities based on research interests, professor details, and project type.

### Sign up and Login Page
The sign-up page allows users to create a new account by providing necessary details such as email, username, and password. The login page enables existing users to access their accounts by entering their credentials, ensuring secure authentication and access to personalized content.

### Search Page
- After logging in, the **Search Page** displays a search bar and different tabs to narrow search results based on professor, project type.
- Users can search directly for professors, projects, or keywords to see available opportunities.

### Searching for Research Opportunities
- **Enter Search Terms**: Type keywords or research areas into the search bar to find related projects or professors.

### Results
- Use tabs to narrow search results based on:
  - **Professor**: Shows projects supervised by specific professors.
  - **Project Type**: VIP/EPICS or professor-mentored projects.

After using the tabs, click **Search** to see refined results.

### Uploading a Resume for Parsing
1. **Navigate to the Resume Parsing Section**: Access this through the main menu.
2. **Upload Resume**: Choose a `.pdf` or `.docx` file from your device.
3. **Parse and Analyze**: Once uploaded, the application will extract text from the resume, highlight key skills, and display the most frequently mentioned keywords.

> **Note**: For optimal parsing, ensure your resume is formatted simply, with clear sections such as **Experience**, **Education**, and **Skills**.

### Usage
1. **Search for Opportunities**: Use the search bar and filters on the homepage to find research opportunities by professors or project areas.
2. **Upload Resume**: Navigate to the Resume section to upload your resume, analyze key terms, and find matching projects.
3. **Refine Results**: Use additional filters to narrow down results based on specific departments, VIP/EPICS project teams, or available positions.

### Example Usage of the Search Engine
<img width="713" alt="image" src="https://github.com/user-attachments/assets/5d81e987-07c5-44a3-bcac-8fa0ef7c81da">

## Example Usage of the Resume Parser
<img width="713" alt="Screenshot 2024-12-09 at 11 10 05 PM" src="https://github.com/user-attachments/assets/75869221-3f0d-436f-9a39-9bd179e8f1fe">
<img width="713" alt="Screenshot 2024-12-09 at 11 10 21 PM" src="https://github.com/user-attachments/assets/7ff682af-edc4-48b9-b0be-c60c2e4fa0e0">



## Architecture
The application follows a multi-tier architecture, consisting of:
1. **Frontend**: User interface for searching and filtering research opportunities.
2. **Backend**: RESTful API for data handling, including resume parsing and data aggregation.
3. **Database**: Stores all research data, professor details, and user information.
4. **Retrieval-Augmented Generation (RAG) Model**: Powers our application by combining retrieval-based document fetching with generative language capabilities, enabling accurate, up-to-date responses without retraining the language model. In the RAG model, the workflow begins with retrieval, where relevant documents are fetched from the vector database based on the query. Next, context building occurs by concatenating these documents with the query to form a comprehensive input. The model then proceeds to generation, where GPT uses this context to produce a coherent, context-aware response. Finally, the output is delivered, providing accurate and relevant results tailored to the user's query.
6. **Web Scraping Module**: Pulls data from university websites and professor pages using `BeautifulSoup` and `Requests`.
7. **Resume Parser Module**: Extracts and analyzes text from user resumes to match with relevant projects.

## Install Dependencies
- Use the following command to install the required Python libraries: `pip install -r requirements.txt`

## Technical Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, REST API
- **Database**: SQLite
- **Web Scraping**: BeautifulSoup, Requests
- **Resume Parsing**: PyPDF2, pdfplumber, NLTK
- **RAG Model**: spaCy, OpenAI's GPT, Haystack, Pinecone, NLTK


## Data Sources
The web application aggregates data from various sources:
1. **Purdue Research Sites**: VIP/EPICS project pages, Purdue faculty directories, etc.
2. **Professor Profiles**: Data pulled directly from Purdue professors' lab websites for up-to-date research information.

## Key Challenges
1. **Data Inconsistency**: Different formatting across resumes and web pages requires adjustments to extraction and parsing logic.
2. **Privacy**: Sensitive data handling for uploaded resumes, mitigated by encryption and access control.

## Support
For assistance or inquiries:  
Contact the team:
- **Stuti Rastogi**: rastogi8@purdue.edu
- **Disha Maheshwari**: dsmahesh@purdue.edu


**Thank you for using the QueryForge!** This tool is designed to make your research search journey easier and more efficient.
