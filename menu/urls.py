from django.urls import path
from menu.controllers.menu_item_controller import MenuItemSaveController, MenuItemGetController, MenuItemListCustomerController, MenuItemListController, MenuItemUpdateController

urlpatterns = [
    path('menuitems/', MenuItemSaveController.as_view(), name="save_menuitem"),
    path('menuitems/find/<int:pk>', MenuItemGetController.as_view(), name="menu_item_find"),
    path('menuitems/list', MenuItemListController.as_view(), name="menu_items_list"),
    path('menuitems/list/<int:pk>', MenuItemListCustomerController.as_view(), name="menu_list_customer"),
    path('menuitems/update/<int:pk>', MenuItemUpdateController.as_view(), name="update_menu_item")
]