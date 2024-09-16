import pytest
import sys
import os

# Add the src directory to the PYTHONPATH
sys.path.insert(0, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '../../backend/app')))
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """Test the home page (/) route."""
    response = client.get('/')
    assert response.status_code == 200
    # Adjust this according to your homepage content
    assert b"Login" in response.data


def test_some_route(client):
    """Test another route (/some_route) in your app."""
    response = client.get('/signup')
    assert response.status_code == 200
    # Adjust to match expected output
    assert b"Sign Up" in response.data
