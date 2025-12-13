import pytest
from unittest.mock import patch, MagicMock
import os
from mailer import send_email
from schemas import NotificationCreate


def test_send_email_success():
    """Test successful email sending"""
    # Set environment variables
    os.environ['SMTP_SERVER'] = 'localhost'
    os.environ['SMTP_PORT'] = '1025'
    os.environ['EMAIL_USER'] = 'test@example.com'
    os.environ['EMAIL_PASS'] = 'password'
    
    notification = NotificationCreate(
        email="recipient@example.com",
        subject="Test Subject",
        text="Test message"
    )
    
    with patch('mailer.smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        
        result = send_email(notification)
        
        assert result == True
        mock_server.send_message.assert_called_once()


def test_send_email_failure():
    """Test failed email sending"""
    notification = NotificationCreate(
        email="recipient@example.com",
        subject="Test Subject",
        text="Test message"
    )
    
    with patch('mailer.smtplib.SMTP') as mock_smtp:
        mock_smtp.side_effect = Exception("Connection failed")
        
        result = send_email(notification)
        
        assert result == False
