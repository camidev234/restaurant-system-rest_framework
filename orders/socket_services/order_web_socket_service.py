from channels.layers import get_channel_layer

class OrderWebSocketService:
    async def send_order_update(self, order_id, status_id):
        """
        Envía un mensaje al grupo de WebSocket basado en el order_id
        para notificar sobre el cambio de estado de la orden.
        """
        channel_layer = get_channel_layer()
        
        channel_layer = get_channel_layer()
        
        # print(f"Channel Layer: {channel_layer}")
        
        group_name = f"group_order_{order_id}"
        # print(f"Sending message to group: {group_name}")


        await channel_layer.group_send(
            group_name, 
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'status_id': status_id,
                'message': "Order status updated"
            }
        )