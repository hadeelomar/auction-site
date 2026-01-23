import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Notification, User


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection"""
        self.user = self.scope["user"]
        
        # Don't allow anonymous users to connect
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return
        
        # Create personal notification group for this user
        self.user_group_name = f"user_{self.user.id}_notifications"
        
        # Join personal group
        await self.channel_layer.group_add(
            self.user_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial unread count
        await self.send_unread_count()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        if hasattr(self, 'user_group_name'):
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(text_data)
            print(f"📨 WebSocket received message from user {self.user.username}: {data}")
            message_type = data.get('type')
            
            if message_type == 'mark_read':
                notification_id = data.get('notification_id')
                if notification_id:
                    print(f"✅ Marking notification {notification_id} as read")
                    await self.mark_notification_read(notification_id)
            elif message_type == 'mark_all_read':
                print(f"✅ Marking all notifications as read")
                await self.mark_all_notifications_read()
            elif message_type == 'get_unread_count':
                print(f"📊 Getting unread count")
                await self.send_unread_count()
                
        except json.JSONDecodeError:
            await self.send_json({
                'type': 'error',
                'message': 'Invalid JSON'
            })
        except Exception as e:
            print(f"❌ Error handling WebSocket message: {e}")
            await self.send_json({
                'type': 'error',
                'message': str(e)
            })
    
    async def notification_message(self, event):
        """Handle new notification messages"""
        await self.send_json({
            'type': 'new_notification',
            'notification': event['notification']
        })
    
    async def unread_count_update(self, event):
        """Handle unread count updates"""
        await self.send_json({
            'type': 'unread_count_update',
            'count': event['count']
        })
    
    async def send_json(self, data):
        """Helper to send JSON messages"""
        await self.send(text_data=json.dumps(data))
    
    async def send_unread_count(self):
        """Send current unread notification count"""
        try:
            count = Notification.objects.filter(
                user=self.user, 
                is_read=False
            ).count()
            
            print(f"📊 Sending unread count for {self.user.username}: {count}")
            
            # Use create_task to avoid blocking
            import asyncio
            asyncio.create_task(
                self.channel_layer.group_send(
                    self.user_group_name,
                    {
                        'type': 'unread_count_update',
                        'count': count
                    }
                )
            )
        except Exception as e:
            print(f"❌ Error sending unread count: {e}")
    
    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Mark a specific notification as read"""
        try:
            notification = Notification.objects.get(
                id=notification_id,
                user=self.user
            )
            notification.is_read = True
            notification.save()
            
            # Send updated unread count
            self.send_unread_count()
            
            return True
        except Notification.DoesNotExist:
            return False
    
    @database_sync_to_async
    def mark_all_notifications_read(self):
        """Mark all notifications as read"""
        try:
            updated = Notification.objects.filter(
                user=self.user,
                is_read=False
            ).update(is_read=True)
            
            # Send updated unread count
            self.send_unread_count()
            
            return updated
        except Exception as e:
            print(f"Error marking all as read: {e}")
            return 0
