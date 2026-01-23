from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from typing import Dict, Any, Optional, Union
from django.contrib.auth.models import User
from .models import Notification


def send_notification_to_user(user_id: int, notification_data: Dict[str, Any]) -> None:
    """
    Send real-time notification to a specific user via WebSocket
    """
    try:
        channel_layer = get_channel_layer()
        group_name = f"user_{user_id}_notifications"
        
        # Send notification to user's personal group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'notification_message',
                'notification': notification_data
            }
        )
    except Exception as e:
        pass


def send_unread_count_update(user_id: int, count: int) -> None:
    """
    Send unread count update to a specific user via WebSocket
    """
    try:
        channel_layer = get_channel_layer()
        group_name = f"user_{user_id}_notifications"
        
        # Send count update to user's personal group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'unread_count_update',
                'count': count
            }
        )
    except Exception as e:
        pass


def create_and_send_notification(user: User, notification_type: str, message: str) -> Optional[Notification]:
    """
    Create notification in database and send via WebSocket
    Includes deduplication to prevent duplicate notifications
    """
    try:
        # Check for existing duplicate notification from the last hour
        from django.utils import timezone
        one_hour_ago = timezone.now() - timezone.timedelta(hours=1)
        
        existing_notification = Notification.objects.filter(
            user=user,
            type=notification_type,
            message=message,
            timestamp__gte=one_hour_ago
        ).first()
        
        if existing_notification:
            return existing_notification
        
        # Create notification in database
        notification = Notification.objects.create(
            user=user,
            type=notification_type,
            message=message
        )
        
        # Prepare notification data for WebSocket
        notification_data = {
            'id': notification.id,
            'type': notification.type,
            'message': notification.message,
            'is_read': notification.is_read,
            'timestamp': notification.timestamp.isoformat(),
        }
        
        # Send real-time notification
        send_notification_to_user(user.id, notification_data)
        
        # Update unread count
        unread_count = Notification.objects.filter(user=user, is_read=False).count()
        send_unread_count_update(user.id, unread_count)
        
        return notification
    except Exception as e:
        return None
