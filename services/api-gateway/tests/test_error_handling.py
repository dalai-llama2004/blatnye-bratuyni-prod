import pytest
import jwt
from unittest.mock import patch, MagicMock
from config import SECRET_KEY


def test_backend_service_error_forwarded(test_client):
    """Test that backend service errors are properly forwarded"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.booking.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.content = b'{"detail": "Invalid slot_id"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/bookings/",
            json={"slot_id": 999},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 400
        assert response.json()["detail"] == "Invalid slot_id"


def test_backend_service_500_error_forwarded(test_client):
    """Test that backend service 500 errors are properly forwarded"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.booking.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.content = b'{"detail": "Internal server error"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/bookings/",
            json={"slot_id": 1},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 500


def test_backend_service_404_error_forwarded(test_client):
    """Test that backend service 404 errors are properly forwarded"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.admin.requests.delete') as mock_delete:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b'{"detail": "Zone not found"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_delete.return_value = mock_response
        
        response = test_client.delete(
            "/admin/zones/999",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404


def test_user_service_registration_error(test_client):
    """Test that user service registration errors are forwarded"""
    with patch('routes.user.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 409
        mock_response.content = b'{"detail": "Email already exists"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/users/register",
            json={"email": "existing@example.com", "password": "password123"}
        )
        
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]


def test_user_service_login_invalid_credentials(test_client):
    """Test that login errors are forwarded"""
    with patch('routes.user.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.content = b'{"detail": "Invalid credentials"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/users/login",
            json={"email": "test@example.com", "password": "wrongpassword"}
        )
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]


def test_notification_service_error(test_client):
    """Test that notification service errors are forwarded"""
    with patch('routes.notification.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.content = b'{"detail": "Invalid email address"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/notifications/",
            json={"email": "invalid-email", "subject": "Test", "body": "Test"}
        )
        
        assert response.status_code == 400


def test_booking_cancel_not_found(test_client):
    """Test that booking cancel returns 404 when booking not found"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.booking.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b'{"detail": "Booking not found"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/bookings/cancel",
            json={"booking_id": 999},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404


def test_extend_booking_not_found(test_client):
    """Test that extend booking returns 404 when booking not found"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.booking.requests.post') as mock_post:
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.content = b'{"detail": "Booking not found"}'
        mock_response.headers = {'content-type': 'application/json'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/bookings/999/extend",
            json={"extend_hours": 1, "extend_minutes": 0},
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 404


def test_get_zones_empty_result(test_client):
    """Test that empty zone list is returned correctly"""
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get("/bookings/zones")
        
        assert response.status_code == 200
        assert response.json() == []


def test_booking_history_empty(test_client):
    """Test that empty booking history is returned correctly"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json() == []


def test_query_params_forwarding(test_client):
    """Test that query parameters are correctly forwarded to backend"""
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1}]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get("/bookings/places/1/slots?date=2024-01-01&start_time=10:00")
        
        assert response.status_code == 200
        # Verify query params were forwarded
        call_args = mock_get.call_args
        assert 'params' in call_args.kwargs
        assert 'date' in call_args.kwargs['params']


def test_content_type_forwarding(test_client):
    """Test that content-type header is correctly forwarded"""
    with patch('routes.user.requests.post') as mock_post:
        # Mock a response with different content type
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"message": "Success"}'
        mock_response.headers = {'content-type': 'text/plain'}
        mock_post.return_value = mock_response
        
        response = test_client.post(
            "/users/register",
            json={"email": "test@example.com", "password": "password123"}
        )
        
        assert response.status_code == 200
        # Verify content-type is forwarded from backend (may include charset)
        assert 'text/plain' in response.headers.get('content-type')


def test_large_booking_history_response(test_client):
    """Test that large responses from backend are handled correctly"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    # Create a large response with 100 bookings
    large_response = [{"id": i, "status": "active"} for i in range(100)]
    
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        import json
        mock_response.content = json.dumps(large_response).encode('utf-8')
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert len(response.json()) == 100
