from django.urls import path
from restaurants.controllers.restaurant_controller import RestaurantSaveController, RestaurantListController, RestaurantGetController, RestaurantUpdateController
from .controllers.menu_category_controller import MenuCategorySaveController, MenuCategoryListController, MenuCategoryGetController, MenuCategoryUpdateController 

urlpatterns = [
    path('restaurants/', RestaurantSaveController.as_view(), name="save_restaurant"),
    path('restaurants/list', RestaurantListController.as_view(), name="restaurant_list"),
    path('restaurants/find/<int:pk>', RestaurantGetController.as_view(), name="restaurant_get"),
    path('restaurants/update/<int:pk>', RestaurantUpdateController.as_view(), name="update_restaurant"),
    path('menu/categories/', MenuCategorySaveController.as_view(), name="save_menu_category"),
    path('menu/categories/list', MenuCategoryListController.as_view(), name="menu_categories_list"),
    path('menu/categories/find/<int:pk>', MenuCategoryGetController.as_view(), name="menu_category_find"),
    path('menu/categories/update/<int:pk>', MenuCategoryUpdateController.as_view(), name="menu_category_update"),
    
]