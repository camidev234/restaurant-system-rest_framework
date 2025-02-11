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
    
    def find_payment_order(self, id):
        try:
            payment_order = PaymentOrder.objects.get(order_gateway_id=id)
            return payment_order
        except PaymentOrder.DoesNotExist as e:
            raise e
        
    def get_order_payment_orders(self, order_id):
        payment_orders = PaymentOrder.objects.filter(order_id=order_id)
        return payment_orders