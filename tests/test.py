import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
import requests

# Testing webscrapping


class TestProfessorScraper(unittest.TestCase):
    @patch('requests.get')
    def test_find_next_info(self, mock_get):
        # Sample HTML content for testing
        html_content = '''
        <html>
            <body>
                <h1>Dr. John Doe</h1>
                <p><strong>Office:</strong> Room 123</p>
                <p><strong>E-mail:</strong> john.doe@university.edu</p>
                <h2>Research</h2>
                <p>Dr. Doe's research focuses on AI and machine learning.</p>
            </body>
        </html>
        '''
        # Mocking requests.get to return a response with sample HTML
        mock_response = MagicMock()
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # Simulate loading the page
        response = requests.get("https://example.com")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Test name extraction
        name = soup.find('h1').get_text(strip=True)
        self.assertEqual(name, "Dr. John Doe")

        # Test office extraction
        office_element = soup.find(string="Office:")
        if office_element:
            office = office_element.find_next(string=True).strip()
            self.assertEqual(office, "Room 123")

        # Test research description extraction
        research_heading = soup.find('h2', string='Research')
        if research_heading:
            research_description = research_heading.find_next(
                'p').get_text(strip=True)
            self.assertEqual(
                research_description,
                "Dr. Doe's research focuses on AI and machine learning.")

    @patch('requests.get')
    def test_missing_labels(self, mock_get):
        # HTML with missing fields for testing edge cases
        html_content = '''
        <html>
            <body>
                <h1>Dr. John Doe</h1>
                <p><strong>Office:</strong></p>
            </body>
        </html>
        '''
        # Mocking requests.get to return a response with sample HTML
        mock_response = MagicMock()
        mock_response.content = html_content
        mock_get.return_value = mock_response

        # Simulate loading the page
        response = requests.get("https://example.com")
        soup = BeautifulSoup(response.content, 'html.parser')

        # Test missing research description
        research_heading = soup.find('h2', string='Research')
        if research_heading:
            research_description = research_heading.find_next(
                'p').get_text(strip=True)
        else:
            research_description = "N/A"
        self.assertEqual(research_description, "N/A")


if __name__ == '__main__':
    unittest.main()
