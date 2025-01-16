from menu.serializers.menu_item_serializers import MenuItemSaveSerializer, MenuItemGetSerializer, MenuItemUpdateSerializer
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from menu.models.menu_item import MenuItem

class MenuItemService:
    
    def save(self, request):
        serializer = MenuItemSaveSerializer(data=request.data, context={"restaurant": request.user.restaurant})
        if serializer.is_valid():
            menu_item_saved = serializer.save()
            menu_item_saved = MenuItemSaveSerializer(menu_item_saved)
            return menu_item_saved.data
        
        raise ValidationError(serializer.errors)
    
    def get_item_instance(self, pk):
        try:
            item = MenuItem.objects.get(id=pk)
            return item
        except MenuItem.DoesNotExist:
            raise NotFound("The item does not exists")
        
    def get_item_by_id(self, pk):
        item = self.get_item_instance(pk)
        serializer = MenuItemGetSerializer(item)
        return serializer.data
    
    def get_all_items(self, request, require_restaurant, pk):
        if require_restaurant:
            if request.user.restaurant:
                items = MenuItem.objects.filter(restaurant_id = request.user.restaurant.id).order_by('id')
                return items
            else:
                raise PermissionDenied("You do not have access to the menu items if you do not belong to a restaurant")
        else:
            items = MenuItem.objects.filter(restaurant_id = pk, active=True).order_by('id')
            return items
        
    def update_by_id(self, pk, data):
        item_to_update = self.get_item_instance(pk)
        serializer = MenuItemUpdateSerializer(item_to_update, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
            
        raise ValidationError(serializer.errors)