from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification_to_user(user_id, notification_data):
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
        print(f"Error sending WebSocket notification: {e}")


def send_unread_count_update(user_id, count):
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
        print(f"Error sending unread count update: {e}")


def create_and_send_notification(user, notification_type, message):
    """
    Create notification in database and send via WebSocket
    """
    try:
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
        print(f"Error creating and sending notification: {e}")
        return None
