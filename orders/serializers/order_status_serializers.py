from rest_framework import serializers
from orders.models.order_status import OrderStatus

class OrderStatusGetSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OrderStatus
        fields = ['id', 'status_name']