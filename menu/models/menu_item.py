from django.db import models
from restaurants.models.menu_category import MenuCategory
from restaurants.models.restaurant import Restaurant 

class MenuItem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=3)
    preparation_time = models.IntegerField()
    image_url = models.CharField(max_length=300, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='menu_items')

    class Meta:
        db_table = 'menu_items'