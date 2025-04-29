import pytest
import json

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test the root route returns successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"System Monitoring" in response.data # Check for a key phrase in the HTML title

def test_metrics_route(client):
    """Test the metrics route returns JSON with cpu and memory."""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert response.content_type == 'application/json'

    data = json.loads(response.data)
    assert 'cpu' in data
    assert 'memory' in data
    assert isinstance(data['cpu'], (int, float))
    assert isinstance(data['memory'], (int, float))