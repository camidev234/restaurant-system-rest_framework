from django.db import transaction
from orders.models.order import Order
from orders.socket_services.payment_web_socket_service import PaymentWebSocketService
from asgiref.sync import async_to_sync

class WebhookPaymentHandler:
    
    @staticmethod
    def handle_charge_succeeded(order_gateway_id, payment_order_service):
        try:
            payment_socket_service = PaymentWebSocketService()
            with transaction.atomic():
                payment_order = payment_order_service.find_payment_order(order_gateway_id)
                
        
                 #if transaction was success, update the order status to 2
        
                order = Order.objects.get(id=payment_order.order.id)
                order.status_id = 2
                order.save()
                
                # update the payment order to "Exitoso"
                
                payment_order.status = "Exitoso"
                payment_order.save()
                
                
                async_to_sync(payment_socket_service.send_payment_status)(payment_order.order_gateway_id, "payment.successful")
                
            return True
                
        except Exception as e:
                print(f"Error to process webhook {e}")
                return False

    @staticmethod
    def handle_charge_cancelled(order_gateway_id, payment_order_service, order_service):
        pass

    @staticmethod
    def handle_charge_failed(order_gateway_id, payment_order_service, order_service):
        pass
