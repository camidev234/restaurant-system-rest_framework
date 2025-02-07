from channels.layers import get_channel_layer 

class PaymentWebSocketService:
    async def send_payment_status(self, payment_order_id, status):
        """
        Envía un mensaje al grupo de WebSocket basado en la orden de pago
        cuando establecio la conexion, para notificar sobre el cambio de estado en el proceso de pago de una orden
        
        args:
            - order_id: id de la orden
            - status_id: id del estado al que cambio la orden,
            - restaurant_id: id del restaurante al que pertenece la orden
        """
        
        channel_layer = get_channel_layer()
        
        group_name = f"payment_status_{payment_order_id}"
        
        await channel_layer.group_send(
            group_name,
            {
                'type': 'order_status_update',
                'payment_order_id': payment_order_id,
                'status': status,
            }
        )