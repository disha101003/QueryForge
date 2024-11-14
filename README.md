## QueryForge
This web application aims to streamline the process of discovering research opportunities within a university setting. By aggregating data on professors, research projects, and student positions from multiple sources, this tool allows students to search for research projects relevant to their interests. 

As students, we understand the challenge of finding research opportunities due to scattered information. This tool provides a centralized database with enhanced search and filtering functionalities, tailored to support students in the ECE department, with plans to expand to additional departments.

## Team Memebers

* Stuti Rastogi
* Disha Maheshwari


## Features
- **Research Opportunity Aggregation**: Gathers data on professors, research projects, and student openings across the ECE department.
- **Resume Parser**: Enables users to upload their resumes, extract key skills and qualifications, and match them with relevant research projects.
- **Advanced Search and Filtering**: Allows users to search and filter opportunities based on research interests, professor details, and project type.
- **User Role Management**: Role-based access control for managing data access and security.

## Architecture
The application follows a multi-tier architecture, consisting of:
1. **Frontend**: User interface for searching and filtering research opportunities.
2. **Backend**: RESTful API for data handling, including resume parsing and data aggregation.
3. **Database**: Stores all research data, professor details, and user information.
4. **Web Scraping Module**: Pulls data from university websites and professor pages using `BeautifulSoup` and `Requests`.
5. **Resume Parser Module**: Extracts and analyzes text from user resumes to match with relevant projects.

## Getting Started
### Prerequisites
- **Python 3.8+**
- **Flask** (for backend)
- **BeautifulSoup** and **Requests** (for web scraping)
- **NLTK** (for resume parsing)
- **PyPDF2** and **pdfplumber** (for PDF handling)
  

## Usage
1. **Search for Opportunities**: Use the search bar and filters on the homepage to find research opportunities by professors or project areas.
2. **Upload Resume**: Navigate to the Resume section to upload your resume, analyze key terms, and find matching projects.
3. **Refine Results**: Use additional filters to narrow down results based on specific departments, VIP/EPICS project teams, or available positions.

## Technical Stack
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask, REST API
- **Database**: SQLite/PostgreSQL
- **Web Scraping**: BeautifulSoup, Requests
- **Resume Parsing**: PyPDF2, pdfplumber, NLTK

## Data Sources
The web application aggregates data from various sources:
1. **University Research Sites**: VIP/EPICS project pages, Purdue faculty directories, etc.
2. **Professor Profiles**: Data pulled directly from Purdue professors' lab websites for up-to-date research information.

## Resume Parser
The resume parser allows users to upload their resumes in `.pdf` or `.docx` format. It:
1. **Extracts Text**: Handles PDF and Word formats using `pdfplumber` and `python-docx`.
2. **Identifies Keywords**: Processes text with `NLTK` to identify high-frequency terms like skills and research interests.
3. **Matches to Projects**: Compares extracted keywords with project descriptions to recommend suitable opportunities.

### Key Challenges
1. **Data Inconsistency**: Different formatting across resumes and web pages requires adjustments to extraction and parsing logic.
2. **Privacy**: Sensitive data handling for uploaded resumes, mitigated by encryption and access control.

To run
* cd into src/backend folder
* run python -m app.app