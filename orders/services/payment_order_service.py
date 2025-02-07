from orders.models.payment_orders import PaymentOrder
from rest_framework.exceptions import NotFound

class PaymentOrderService:
    
    def save_payment_order(self, order):
        payment_order = PaymentOrder()
        payment_order.order = order
        payment_order.save()
        
        payment_order.order_gateway_id = f"order{order.id}{payment_order.id}"
        payment_order.save()
        
        
        return payment_order
    
    def assign_order_transaction(self, payment_order, transaction_id):
        payment_order.transaction_id = transaction_id
        payment_order.save()
        
        return True
    
    def find_payment_order(self, id):
        try:
            payment_order = PaymentOrder.objects.get(order_gateway_id=id)
            return payment_order
        except PaymentOrder.DoesNotExist:
            raise NotFound("The order does not found, please check the number")