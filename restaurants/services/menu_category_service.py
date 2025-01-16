from rest_framework.exceptions import ValidationError, NotFound
from restaurants.serializers.menu_category_serializers import MenuCategorySaveSerializer, MenuCategoryGetSerializer, MenuCategoryUpdateSerializer
from restaurants.models.menu_category import MenuCategory

class MenuCategoryService:
    
    def save(self, data, user_auth):
        restaurant = user_auth.restaurant
        serializer = MenuCategorySaveSerializer(data=data, context={"restaurant": restaurant})
        
        if serializer.is_valid():
            menu_category_saved = serializer.save()
            menu_category_saved = MenuCategorySaveSerializer(menu_category_saved)
            return menu_category_saved.data
            
        raise ValidationError(serializer.errors)
    
    def get_all_menu_categories(self, request):
        if request.user.restaurant:
            categories = MenuCategory.objects.filter(restaurant_id=request.user.restaurant.id).order_by('id')
            return categories
        else:
            categories = MenuCategory.objects.all().order_by('id')
            return categories
        
    def get_menu_category_instance(self, pk):
        try:
            menu_category = MenuCategory.objects.get(id=pk)
            return menu_category
        except MenuCategory.DoesNotExist:
            raise NotFound("The menu category does not exists")
        
    def get_by_id(self, id):
        category = self.get_menu_category_instance(id)
        category_serialized = MenuCategoryGetSerializer(category)
        return category_serialized.data
         
         
    def update_by_id(self, data, id):
        category_to_update = self.get_menu_category_instance(id)
        category_updated = MenuCategoryUpdateSerializer(category_to_update, data=data)
        if category_updated.is_valid():
            category_updated.save()
            return category_updated.data
        
        raise ValidationError(category_updated.errors)
            