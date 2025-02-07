import json
from channels.generic.websocket import AsyncWebsocketConsumer
from users.services.user_service import UserService
from asgiref.sync import sync_to_async

class PaymentConsumer(AsyncWebsocketConsumer):

    async def connect(self): 
        user = self.scope.get("user")
        if user.is_anonymous:
            await self.close()
        
        self.payment_order_id = self.scope["url_route"]["kwargs"]["payment_order_id"]
        self.group_name = f"payment_status_{self.payment_order_id}"
        
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
        order_id = event["payment_order_id"]
        status = event["status"]
        message = event["message"]
        
        await self.send(text_data=json.dumps({
            "payment_order_id": order_id,
            "status": status,
            "message": message,
        }))      

