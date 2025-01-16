from rest_framework import serializers

from users.models import User, Typology
from .typology_serializers import TypologyInfoSerializer
from restaurants.models import Restaurant

#serializer for GET requests
class UserGetSerializer(serializers.ModelSerializer):
    
    restaurant_id = serializers.PrimaryKeyRelatedField(
        source = "restaurant",
        read_only = True
    )

    typology = TypologyInfoSerializer(read_only=True)
    active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'typology', 'restaurant_id', 'active', 'created_at']

#Serializer for POST requests
class UserSerializer(serializers.ModelSerializer):
    
    #map the field typology_id as typology field in the model
    # Only POST requests
    typology_id = serializers.PrimaryKeyRelatedField(
        queryset = Typology.objects.all(),
        source = "typology",
        # write_only = True
    )
    
    #restaurant_id in POST requests
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset = Restaurant.objects.all(),
        source = "restaurant",
        # write_only = True,
        required = False
    )
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'typology_id', 'restaurant_id']

class UserUpdateSerializer(serializers.ModelSerializer):
    
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset = Restaurant.objects.all(),
        source = "restaurant",
        required = False
    )
    
    typology_id = serializers.PrimaryKeyRelatedField(
        queryset=Typology.objects.all(),
        source = "typology",
        required = False
    )
    
    active = serializers.BooleanField(required=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'typology_id', 'restaurant_id', 'active']
               
               
class UserUpdatePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length=8, required=True)
    
    class Meta:
        model = User
        fields = ['password']   