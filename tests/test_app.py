import pytest
from app import app, weather_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        # Clean up / reset environment after tests
        weather_data.clear()

def test_add_weather(client):
    """
    Test adding weather data.
    - Adds data via a POST request and checks if it's stored correctly.
    """
    response = client.post('/add', data={'temperature': '20', 'humidity': '50'}, follow_redirects=True)
    assert response.status_code == 200
    assert '20' in response.data.decode()
    assert '50' in response.data.decode()
    assert len(weather_data) == 1

def test_view_weather(client):
    """
    Test viewing weather data.
    - Ensures the index page includes the added data.
    """
    client.post('/add', data={'temperature': '20', 'humidity': '50'})
    response = client.get('/')
    assert '20' in response.data.decode()
    assert '50' in response.data.decode()

def test_analysis_average_temperature(client):
    """
    Test calculation of average temperature.
    - Adds several data points, calculates the average, and checks if it’s returned correctly.
    """
    client.post('/add', data={'temperature': '20', 'humidity': '50'})
    client.post('/add', data={'temperature': '30', 'humidity': '55'})
    response = client.get('/analysis')
    assert response.status_code == 200
    data = response.json
    expected_average = (20 + 30) / 2.0
    assert data['average_temperature'] == expected_average