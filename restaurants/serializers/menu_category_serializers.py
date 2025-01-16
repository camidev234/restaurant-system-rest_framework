from rest_framework import serializers
from restaurants.models.menu_category import MenuCategory
from restaurants.models.restaurant import Restaurant

class MenuCategorySaveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'category_name']
        
    def create(self, validated_data):
        restaurant = self.context.get('restaurant')
        if not restaurant:
            raise serializers.ValidationError("Restaurant context is required.")
   
        return MenuCategory.objects.create(restaurant=restaurant, **validated_data)
    
class MenuCategoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ['id', 'category_name', 'created_at', 'active']
        
class MenuCategoryUpdateSerializer(serializers.ModelSerializer):
    
    active = serializers.BooleanField(required=True)
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'category_name', 'active']