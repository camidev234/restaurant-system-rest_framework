from django.db import models
from users.models.users import User
from orders.models.order_status import OrderStatus
from restaurants.models import Restaurant

class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    special_instructions = models.TextField(null=True, blank=True)
    
    dealer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dealer_orders', null=True, blank=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='orders', default=1)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    class Meta:
        db_table="orders"
