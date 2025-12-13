import pytest
import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY


def test_valid_token_authentication(test_client):
    """Test that valid JWT token is accepted"""
    from unittest.mock import patch, MagicMock
    
    # Create a valid token
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service response
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1}]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200


def test_expired_token_authentication(test_client):
    """Test that expired JWT token is rejected with 401"""
    from unittest.mock import patch, MagicMock
    
    # Create an expired token (expired 1 hour ago)
    expired_payload = {
        'user_id': 1,
        'sub': 1,
        'role': 'user',
        'exp': datetime.now(timezone.utc) - timedelta(hours=1)
    }
    token = jwt.encode(expired_payload, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 401
        assert "expired" in response.json()["detail"].lower()
        # Backend should not be called for expired token
        mock_get.assert_not_called()


def test_invalid_token_format(test_client):
    """Test that invalid JWT token format is rejected with 401"""
    from unittest.mock import patch, MagicMock
    
    # Invalid token format
    invalid_token = "this-is-not-a-valid-jwt-token"
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        
        assert response.status_code == 401
        assert "Invalid JWT token" in response.json()["detail"]
        # Backend should not be called for invalid token
        mock_get.assert_not_called()


def test_malformed_token(test_client):
    """Test that malformed JWT token is rejected with 401"""
    from unittest.mock import patch, MagicMock
    
    # Malformed token (invalid base64)
    malformed_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {malformed_token}"}
        )
        
        assert response.status_code == 401
        assert "Invalid JWT token" in response.json()["detail"]
        mock_get.assert_not_called()


def test_wrong_secret_token(test_client):
    """Test that token signed with wrong secret is rejected"""
    from unittest.mock import patch, MagicMock
    
    # Token signed with wrong secret
    wrong_secret_token = jwt.encode(
        {'user_id': 1, 'sub': 1, 'role': 'user'},
        "wrong-secret-key",
        algorithm='HS256'
    )
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {wrong_secret_token}"}
        )
        
        assert response.status_code == 401
        assert "Invalid JWT token" in response.json()["detail"]
        mock_get.assert_not_called()


def test_missing_authorization_header(test_client):
    """Test that request without Authorization header is rejected with 401"""
    from unittest.mock import patch, MagicMock
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        response = test_client.get("/bookings/history")
        
        # FastAPI HTTPBearer returns 401 when header is missing
        assert response.status_code == 401
        mock_get.assert_not_called()


def test_invalid_authorization_scheme(test_client):
    """Test that non-Bearer authorization scheme is rejected"""
    from unittest.mock import patch, MagicMock
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service (should not be called)
    with patch('routes.booking.requests.get') as mock_get:
        # Using Basic auth instead of Bearer
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Basic {token}"}
        )
        
        # Should be rejected by HTTPBearer
        assert response.status_code == 401
        mock_get.assert_not_called()


def test_token_with_user_id_as_sub(test_client):
    """Test that token with user_id in 'sub' field works correctly"""
    from unittest.mock import patch, MagicMock
    
    # Token with user_id as 'sub' (common JWT standard)
    token = jwt.encode({'sub': 42, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service response
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1}]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        # Verify the user_id was correctly extracted from 'sub'
        call_args = mock_get.call_args
        assert call_args.kwargs['headers']['X-User-Id'] == '42'


def test_token_without_role_defaults_to_user(test_client):
    """Test that token without role field defaults to 'user' role"""
    from unittest.mock import patch, MagicMock
    
    # Token without role field
    token = jwt.encode({'user_id': 1, 'sub': 1}, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service response
    with patch('routes.booking.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1}]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/bookings/history",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        # Verify the role defaults to 'user'
        call_args = mock_get.call_args
        assert call_args.kwargs['headers']['X-User-Role'] == 'user'


def test_admin_token_authentication(test_client):
    """Test that admin token is correctly processed"""
    from unittest.mock import patch, MagicMock
    
    # Admin token
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    # Mock the backend service response
    with patch('routes.admin.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'[{"id": 1}]'
        mock_response.headers = {'content-type': 'application/json'}
        mock_get.return_value = mock_response
        
        response = test_client.get(
            "/admin/zones",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        # Verify admin role is passed correctly
        call_args = mock_get.call_args
        assert call_args.kwargs['headers']['X-User-Role'] == 'admin'
