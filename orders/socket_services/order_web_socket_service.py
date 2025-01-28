from channels.layers import get_channel_layer

class OrderWebSocketService:
    async def send_order_update(self, order_id, status_id):
        """
        Envía un mensaje al grupo de WebSocket basado en el order_id
        para notificar sobre el cambio de estado de la orden.
        
        args:
            - order_id: id de la orden
            - status_id: id del estado al que cambio la orden
        """
        channel_layer = get_channel_layer()
        
        group_name = f"group_order_{order_id}"

        await channel_layer.group_send(
            group_name, 
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'status_id': status_id,
                'message': "Order status updated"
            }
        )
        
    async def send_order_list_restaurant_update(self, order_id, status_id, restaurant_id):
        """
        Envía un mensaje al grupo de WebSocket basado en el restaurante al que petenece al usuario
        cuando establecio la conexion, para notificar sobre el cambio de estado de la orden.
        
        args:
            - order_id: id de la orden
            - status_id: id del estado al que cambio la orden,
            - restaurant_id: id del restaurante al que pertenece la orden
        """
        
        channel_layer = get_channel_layer()
        
        group_name = f"order_list_restaurant_{restaurant_id}"
        
        await channel_layer.group_send(
            group_name,
            {
                'type': 'order_status_update',
                'order_id': order_id,
                'status_id': status_id,
                'message': "Order status updated"
            }
        )