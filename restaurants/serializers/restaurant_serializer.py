from rest_framework import serializers
from restaurants.models.restaurant import Restaurant

class RestaurantSaveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'category', 'latitude', 'longitude']
        
        
class RestaurantGetSerializer(serializers.ModelSerializer):
       
    class Meta:   
        model = Restaurant
        fields = ['id', 'name', 'address', 'category', 'latitude', 'longitude', 'created_at', 'active']
        

class RestaurantUpdateSerializer(serializers.ModelSerializer):
       
    active = serializers.BooleanField(required=True)
    latitude=serializers.DecimalField(required=False, max_digits=21, decimal_places=11)
    longitude=serializers.DecimalField(required=False, max_digits=21, decimal_places=11)
       
    class Meta:   
        model = Restaurant
        fields = ['id', 'name', 'address', 'category', 'latitude', 'longitude', 'active']