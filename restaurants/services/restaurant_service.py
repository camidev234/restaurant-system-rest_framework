from restaurants.serializers.restaurant_serializer import RestaurantSaveSerializer, RestaurantGetSerializer, RestaurantUpdateSerializer
from rest_framework.exceptions import ValidationError, NotFound
from restaurants.models.restaurant import Restaurant

class RestaurantService:
    
    def save(self, data):
        serializer = RestaurantSaveSerializer(data=data)
        if serializer.is_valid():
                restaurant_created = serializer.save()
                restaurant_serialized = RestaurantSaveSerializer(restaurant_created)
                return restaurant_serialized.data
            
        raise ValidationError(serializer.errors)
    
    def get_all_restaurants(self):
        restaurants = Restaurant.objects.all().order_by('id')
        return restaurants
    
    def get_restaurant_instance(self, id):
        try:
            restaurant = Restaurant.objects.get(id=id)
            return restaurant
        except Restaurant.DoesNotExist:
            raise NotFound("Restaurant does not exists")
        
    def get_by_id(self, id):
        restaurant = self.get_restaurant_instance(id)
        restaurant_serialized = RestaurantGetSerializer(restaurant)
        return restaurant_serialized.data
    
    def update_by_id(self, data, id):
        restaurant_to_update = self.get_restaurant_instance(id)
        restaurant_updated = RestaurantUpdateSerializer(restaurant_to_update, data=data)
        if restaurant_updated.is_valid():
            restaurant_updated.save()
            return restaurant_updated.data
        
        raise ValidationError(restaurant_updated.errors)