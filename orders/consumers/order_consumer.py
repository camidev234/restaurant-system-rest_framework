import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if user.is_anonymous:
            await self.close()

        self.order_id = self.scope["url_route"]["kwargs"]["order_id"]
        self.group_name = f"group_order_{self.order_id}"
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
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
        