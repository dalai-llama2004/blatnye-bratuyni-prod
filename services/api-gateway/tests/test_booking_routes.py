import pytest
import jwt
from unittest.mock import patch, MagicMock
from config import SECRET_KEY


@patch('routes.booking.requests.get')
def test_get_places_in_zone(mock_get, test_client):
    """Test get places in zone endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "name": "Place 1"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    response = test_client.get("/bookings/zones/1/places")
    
    assert response.status_code == 200
    mock_get.assert_called_once()


@patch('routes.booking.requests.get')
def test_get_slots(mock_get, test_client):
    """Test get slots endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "start_time": "2024-01-01T10:00:00"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    response = test_client.get("/bookings/places/1/slots")
    
    assert response.status_code == 200
    mock_get.assert_called_once()


@patch('routes.booking.requests.post')
def test_create_booking(mock_post, test_client):
    """Test create booking endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.content = b'{"id": 1, "status": "active"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/bookings/",
        json={"slot_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    mock_post.assert_called_once()


@patch('routes.booking.requests.post')
def test_create_booking_by_time(mock_post, test_client):
    """Test create booking by time endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.content = b'{"id": 1, "status": "active"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/bookings/by-time",
        json={"zone_id": 1, "date": "2024-01-01", "start_hour": 10, "start_minute": 0, "end_hour": 12, "end_minute": 0},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    mock_post.assert_called_once()


@patch('routes.booking.requests.post')
def test_cancel_booking(mock_post, test_client):
    """Test cancel booking endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Booking cancelled"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/bookings/cancel",
        json={"booking_id": 1},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


@patch('routes.booking.requests.get')
def test_booking_history(mock_get, test_client):
    """Test booking history endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "status": "active"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.get(
        "/bookings/history",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_get.assert_called_once()
