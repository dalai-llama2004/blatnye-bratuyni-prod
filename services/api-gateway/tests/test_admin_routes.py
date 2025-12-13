import pytest
import jwt
from unittest.mock import patch, MagicMock
from config import SECRET_KEY


@patch('routes.admin.requests.post')
def test_create_zone(mock_post, test_client):
    """Test create zone admin endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.content = b'{"id": 1, "name": "New Zone"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/admin/zones",
        json={"name": "New Zone", "address": "Test Address"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    mock_post.assert_called_once()


@patch('routes.admin.requests.patch')
def test_update_zone(mock_patch, test_client):
    """Test update zone admin endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"id": 1, "name": "Updated Zone"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_patch.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.patch(
        "/admin/zones/1",
        json={"name": "Updated Zone"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_patch.assert_called_once()


@patch('routes.admin.requests.delete')
def test_delete_zone(mock_delete, test_client):
    """Test delete zone admin endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Zone deleted"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_delete.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.delete(
        "/admin/zones/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_delete.assert_called_once()


@patch('routes.admin.requests.post')
def test_close_zone(mock_post, test_client):
    """Test close zone admin endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'{"message": "Zone closed"}'
    mock_response.headers = {'content-type': 'application/json'}
    mock_post.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.post(
        "/admin/zones/1/close",
        json={"closure_reason": "Maintenance"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_post.assert_called_once()


@patch('routes.admin.requests.get')
def test_get_zones_admin(mock_get, test_client):
    """Test get zones admin endpoint"""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b'[{"id": 1, "name": "Zone 1"}]'
    mock_response.headers = {'content-type': 'application/json'}
    mock_get.return_value = mock_response
    
    token = jwt.encode({'user_id': 1, 'sub': 1, 'role': 'admin'}, SECRET_KEY, algorithm='HS256')
    
    response = test_client.get(
        "/admin/zones",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    mock_get.assert_called_once()


def test_options_zones(test_client):
    """Test OPTIONS for zones endpoint"""
    response = test_client.options("/admin/zones")
    assert response.status_code == 200


def test_options_zone(test_client):
    """Test OPTIONS for specific zone endpoint"""
    response = test_client.options("/admin/zones/1")
    assert response.status_code == 200


def test_options_zone_close(test_client):
    """Test OPTIONS for zone close endpoint"""
    response = test_client.options("/admin/zones/1/close")
    assert response.status_code == 200
