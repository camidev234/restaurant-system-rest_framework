from rest_framework import serializers
from menu.models.menu_item import MenuItem
from restaurants.models.menu_category import MenuCategory
from restaurants.serializers.menu_category_serializers import MenuCategoryGetSerializer

class MenuItemSaveSerializer(serializers.ModelSerializer):
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(),
        source="category",
        required=True
    )
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'preparation_time', 'image_url', 'category_id']
        
    def create(self, validated_data):
        restaurant = self.context.get('restaurant')
        if not restaurant:
            raise serializers.ValidationError("Restaurant context is required.")
   
        return MenuItem.objects.create(restaurant=restaurant, **validated_data)
    
class MenuItemGetSerializer(serializers.ModelSerializer):
    
    category = MenuCategoryGetSerializer(read_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'preparation_time', 'image_url', 'category', 'restaurant_id', "active"]


class MenuItemUpdateSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=MenuCategory.objects.all(),
        source="category",
        required=True
    )
    
    active = serializers.BooleanField(required=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'preparation_time', 'image_url', 'category_id', 'active']