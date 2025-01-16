from rest_framework import serializers
from orders.models.order_item import OrderItem

class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=True)
    quantity = serializers.IntegerField(required=True, min_value=1)
    
    class Meta:
        fields = ['id', 'quantity']
        
class OrderItemGetSerializer(serializers.Serializer):
    
    id = serializers.IntegerField(required=True)
    menu_item_id = serializers.IntegerField(required=True)
    item_name = serializers.CharField()
    description = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=3)
    category_name = serializers.CharField(required=True)
    image_url = serializers.CharField(required=True)
    quantity = serializers.IntegerField(required=True)
    active = serializers.BooleanField(required=True)
    created = serializers.DateTimeField(required=True)
    
    
    class Meta:
        fields = ['id', 'menu_item_id', 'item_name', 'description', 'price', 'category_name', 'image_url', 'quantity', 'active', 'created']