import json
from channels.generic.websocket import AsyncWebsocketConsumer
from users.services.user_service import UserService
from asgiref.sync import sync_to_async

class OrderListConsumer(AsyncWebsocketConsumer):

    async def connect(self): 
        user = self.scope.get("user")
        if user.is_anonymous:
            await self.close()
        
        self.group_name = f"order_list_restaurant_{user.restaurant_id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
        self.close()
        
        
    async def order_status_update(self, event):
        order_id = event["order_id"]
        status_id = event["status_id"]
        message = event["message"]
        status_name = event["status_name"]
        
        await self.send(text_data=json.dumps({
            "order_id": order_id,
            "status_id": status_id,
            "message": message,
            "status_name": status_name
        }))      

