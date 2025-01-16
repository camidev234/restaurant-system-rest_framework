from django.db import models
from restaurants.models.restaurant import Restaurant

class MenuCategory(models.Model):
    
    category_name = models.CharField(max_length=40)
    active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = "menu_categories"