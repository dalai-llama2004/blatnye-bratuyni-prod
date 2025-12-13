import pytest
from unittest.mock import patch, MagicMock


@patch('routes.user.requests.post')
def test_confirm_user(mock_post, test_client):
    """Test user email confirmation endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Email confirmed"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    response = test_client.post(
        "/users/confirm",
        json={"code": "123456"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


@patch('routes.user.requests.post')
def test_recover_password(mock_post, test_client):
    """Test password recovery endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Recovery email sent"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    response = test_client.post(
        "/users/recover",
        json={"email": "test@example.com"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


@patch('routes.user.requests.post')
def test_reset_password(mock_post, test_client):
    """Test password reset endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Password reset"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    response = test_client.post(
        "/users/reset",
        json={"code": "123456", "password": "newpassword123"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()
