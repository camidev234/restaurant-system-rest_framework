from orders.models.payment_orders import PaymentOrder

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