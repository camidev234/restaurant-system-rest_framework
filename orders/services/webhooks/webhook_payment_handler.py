from django.db import transaction
from orders.models.order import Order
from orders.models.payment_orders import PaymentOrder
from orders.socket_services.payment_web_socket_service import PaymentWebSocketService
from asgiref.sync import async_to_sync
from rest_framework.exceptions import NotFound
from orders.socket_services.order_web_socket_service import OrderWebSocketService

class WebhookPaymentHandler:
    
    @staticmethod
    def handle_charge_succeeded(order_gateway_id, payment_order_service):
        try:
            with transaction.atomic():
                payment_order = payment_order_service.find_payment_order(order_gateway_id)
                order = Order.objects.get(id=payment_order.order.id)
                
                order_payment_orders_paid = payment_order_service.get_order_payment_orders(order.id).filter(status="Exitoso")
                if not order_payment_orders_paid:
                    order.status_id = 1
                    order.save()

                    payment_order.status = "Exitoso"
                    payment_order.save()

            try:
                payment_socket_service = PaymentWebSocketService()
                order_web_socket_service = OrderWebSocketService()

                async_to_sync(payment_socket_service.send_payment_status)(
                    payment_order.order_gateway_id, 
                    "payment.successful"
                )
                async_to_sync(order_web_socket_service.send_order_list_restaurant_update)(
                    order.id, 
                    order.status_id, 
                    order.restaurant_id, 
                    order.status.status_name
                )
                async_to_sync(order_web_socket_service.send_order_update)(
                    order.id, 
                    order.status_id, 
                    order.status.status_name
                )
            except Exception as ws_error:
                print(f"Error al enviar sockets: {ws_error}")

            return True
                
        except PaymentOrder.DoesNotExist:
            raise NotFound("The payment order does not exist")
        except Order.DoesNotExist:
            raise NotFound(f"There is no order associated with this order_id {order_gateway_id}")
        except Exception as e:
            print(f"Error al procesar webhook: {e}")

    @staticmethod
    def handle_charge_cancelled(order_gateway_id, payment_order_service):
        try:
            payment_socket_service = PaymentWebSocketService()
            payment_order = payment_order_service.find_payment_order(order_gateway_id)

            payment_order.status = "Cancelado"
            payment_order.save()
            
            async_to_sync(payment_socket_service.send_payment_status)(
                    payment_order.order_gateway_id, 
                    "payment.successful"
                )
            return True
        except Exception as e:
            print(f"Error to process webhook {e}")
            return False    
        
    @staticmethod
    def handle_charge_failed(order_gateway_id, payment_order_service):
        try:
            payment_socket_service = PaymentWebSocketService()
            payment_order = payment_order_service.find_payment_order(order_gateway_id)

            payment_order.status = "FALLIDO"
            payment_order.save()
            
            async_to_sync(payment_socket_service.send_payment_status)(
                payment_order.order_gateway_id, 
                "payment.failed"
            )
                
            return True
        except Exception as e:
            print(f"Error to process webhook {e}")
            return False    
         
