from django.db import models
from orders.models.order import Order

class PaymentOrder(models.Model):
    
    STATUS_CHOICES = [
        ("PENDIENTE", "Pendiente"),
        ("EXITOSO", "Exitoso"),
        ("FALLIDO", "FALLIDO"),
        ("CANCELADO", "Cancelado")
    ]
    
    order_gateway_id = models.CharField(unique=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payment_orders")
    transaction_id = models.CharField(max_length=150, unique=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pendiente"
    )
    
    class Meta:
        db_table="payment_orders"