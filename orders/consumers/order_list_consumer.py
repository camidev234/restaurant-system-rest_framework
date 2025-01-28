import json
from channels.generic.websocket import AsyncWebsocketConsumer
from users.services.user_service import UserService

class OrderListConsumer(AsyncWebsocketConsumer):

    async def connect(self): 
        user = self.scope.get("user")
        if user.is_anonymous:
            await self.close()
        
        user = UserService().get_user_instance(user.id)
        
        self.group_name = f"order_list_restaurant_{user.restaurant.id}"
        
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
        
        await self.send(text_data=json.dumps({
            "order_id": order_id,
            "status_id": status_id,
            "message": message
        }))      

