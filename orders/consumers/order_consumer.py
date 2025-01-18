import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
     
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
        
        
    # async def receive(self, text_data):
    #     data = json.loads(text_data)
    #     message = data.get("message", "")
        
    #     await self.channel_layer.group_send(
    #         self.group_name,
    #         {
    #             "type": "order_status_update",
    #             "message": message
    #         }
    #     )
        
    async def order_status_update(self, event):
        order_id = event["order_id"]
        status_id = event["status_id"]
        message = event["message"]
        
        await self.send(text_data=json.dumps({
            "order_id": order_id,
            "status_id": status_id,
            "message": message
        }))        
        