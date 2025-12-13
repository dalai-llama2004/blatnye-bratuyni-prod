import pytest
import jwt
from unittest.mock import patch, MagicMock
from config import SECRET_KEY


@patch('routes.notification.requests.post')
def test_notify(mock_post, test_client):
    """Test notification endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Notification sent"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    response = test_client.post(
        "/notifications/",
        json={"email": "test@example.com", "subject": "Test", "body": "Test message"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


@patch('routes.notification.requests.post')
def test_bulk_notify_admin(mock_post, test_client):
    """Test bulk notification endpoint for admin"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Bulk notifications sent"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/notifications/bulk",
        json={"subject": "Test", "body": "Test message"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


def test_bulk_notify_non_admin(test_client):
    """Test bulk notification endpoint for non-admin user (should fail)"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/notifications/bulk",
        json={"subject": "Test", "body": "Test message"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403


@patch('routes.notification.requests.get')
def test_get_user_notifications_own(mock_get, test_client):
    """Test get user notifications for own user"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "subject": "Test"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.get(
        "/notifications/user/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_get.assert_called_once()


def test_get_user_notifications_other_user(test_client):
    """Test get user notifications for other user (should fail)"""
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'user'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.get(
        "/notifications/user/2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 403


@patch('routes.notification.requests.get')
def test_get_user_notifications_admin(mock_get, test_client):
    """Test get user notifications for admin (should succeed for any user)"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "subject": "Test"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.get(
        "/notifications/user/2",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_get.assert_called_once()


def test_options_bulk(test_client):
    """Test OPTIONS for bulk notifications endpoint"""
    response = test_client.options("/notifications/bulk")
    assert response.status_code == 200


def test_options_user_notifications(test_client):
    """Test OPTIONS for user notifications endpoint"""
    response = test_client.options("/notifications/user/1")
    assert response.status_code == 200
