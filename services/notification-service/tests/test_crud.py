import pytest
import crud


def test_create_notification(test_db):
    """Test creating a notification"""
    notif = crud.create_notification(
        db=test_db,
        user_id=1,
        type="info",
        title="Test Notification",
        message="Test message"
    )
    
    assert notif.id is not None
    assert notif.user_id == 1
    assert notif.type == "info"
    assert notif.title == "Test Notification"
    assert notif.message == "Test message"
    assert notif.sent == False


def test_get_unsent_notifs(test_db):
    """Test getting unsent notifications"""
    # Create sent and unsent notifications
    notif1 = crud.create_notification(
        db=test_db,
        user_id=1,
        type="info",
        title="Unsent",
        message="This is unsent"
    )
    
    notif2 = crud.create_notification(
        db=test_db,
        user_id=2,
        type="info",
        title="Sent",
        message="This is sent"
    )
    crud.mark_notification_sent(test_db, notif2.id)
    
    unsent = crud.get_unsent_notifs(test_db)
    
    assert len(unsent) >= 1
    assert notif1.id in [n.id for n in unsent]
    assert notif2.id not in [n.id for n in unsent]


def test_get_user_notifications(test_db):
    """Test getting user notifications"""
    # Create notifications for different users
    notif1 = crud.create_notification(
        db=test_db,
        user_id=1,
        type="info",
        title="User 1 Notif 1",
        message="Message 1"
    )
    
    notif2 = crud.create_notification(
        db=test_db,
        user_id=1,
        type="warning",
        title="User 1 Notif 2",
        message="Message 2"
    )
    
    notif3 = crud.create_notification(
        db=test_db,
        user_id=2,
        type="info",
        title="User 2 Notif",
        message="Message for user 2"
    )
    
    user1_notifs = crud.get_user_notifications(test_db, user_id=1)
    user2_notifs = crud.get_user_notifications(test_db, user_id=2)
    
    assert len(user1_notifs) >= 2
    assert len(user2_notifs) >= 1
    assert all(n.user_id == 1 for n in user1_notifs)
    assert all(n.user_id == 2 for n in user2_notifs)


def test_mark_notification_sent(test_db):
    """Test marking notification as sent"""
    notif = crud.create_notification(
        db=test_db,
        user_id=1,
        type="info",
        title="Test",
        message="Test message"
    )
    
    assert notif.sent == False
    
    updated = crud.mark_notification_sent(test_db, notif.id)
    
    assert updated.sent == True


def test_mark_notification_sent_nonexistent(test_db):
    """Test marking nonexistent notification as sent"""
    result = crud.mark_notification_sent(test_db, 99999)
    assert result is None


def test_get_user_notifications_limit(test_db):
    """Test getting user notifications with limit"""
    # Create many notifications
    for i in range(60):
        crud.create_notification(
            db=test_db,
            user_id=10,
            type="info",
            title=f"Notification {i}",
            message=f"Message {i}"
        )
    
    # Get with default limit (50)
    notifs = crud.get_user_notifications(test_db, user_id=10)
    assert len(notifs) == 50
    
    # Get with custom limit
    notifs_10 = crud.get_user_notifications(test_db, user_id=10, limit=10)
    assert len(notifs_10) == 10
