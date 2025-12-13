import pytest
import os
from config import SECRET_KEY, USER_SERVICE_URL, BOOKING_SERVICE_URL, NOTIFICATION_SERVICE_URL


def test_secret_key_environment_variable():
    """Test that SECRET_KEY is loaded from JWT_SECRET environment variable"""
    # The default value should be set
    assert SECRET_KEY is not None
    assert len(SECRET_KEY) > 0
    
    # If JWT_SECRET is not set, should use default
    if 'JWT_SECRET' not in os.environ:
        assert SECRET_KEY == "a-string-secret-at-least-256-bits-long"


def test_user_service_url_configuration():
    """Test that USER_SERVICE_URL is properly configured"""
    assert USER_SERVICE_URL is not None
    assert USER_SERVICE_URL.startswith("http")
    # Default value or custom value from environment
    assert "user-service" in USER_SERVICE_URL or os.environ.get("USER_SERVICE_URL") == USER_SERVICE_URL


def test_booking_service_url_configuration():
    """Test that BOOKING_SERVICE_URL is properly configured"""
    assert BOOKING_SERVICE_URL is not None
    assert BOOKING_SERVICE_URL.startswith("http")
    # Default value or custom value from environment
    assert "booking-service" in BOOKING_SERVICE_URL or os.environ.get("BOOKING_SERVICE_URL") == BOOKING_SERVICE_URL


def test_notification_service_url_configuration():
    """Test that NOTIFICATION_SERVICE_URL is properly configured"""
    assert NOTIFICATION_SERVICE_URL is not None
    assert NOTIFICATION_SERVICE_URL.startswith("http")
    # Default value or custom value from environment
    assert "notification-service" in NOTIFICATION_SERVICE_URL or os.environ.get("NOTIFICATION_SERVICE_URL") == NOTIFICATION_SERVICE_URL


def test_all_configurations_non_empty():
    """Test that all configuration values are non-empty strings"""
    configs = {
        'SECRET_KEY': SECRET_KEY,
        'USER_SERVICE_URL': USER_SERVICE_URL,
        'BOOKING_SERVICE_URL': BOOKING_SERVICE_URL,
        'NOTIFICATION_SERVICE_URL': NOTIFICATION_SERVICE_URL,
    }
    
    for config_name, config_value in configs.items():
        assert isinstance(config_value, str), f"{config_name} should be a string"
        assert len(config_value) > 0, f"{config_name} should not be empty"


def test_service_urls_different():
    """Test that all service URLs are different (no copy-paste errors)"""
    urls = {USER_SERVICE_URL, BOOKING_SERVICE_URL, NOTIFICATION_SERVICE_URL}
    # All three URLs should be unique
    assert len(urls) == 3, "Service URLs should be unique"
