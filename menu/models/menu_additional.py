from django.db import models
from .menu_item import MenuItem


class MenuAdditional(models.Model):
    menu_item = models.ForeignKey(MenuItem, related_name="additionals", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_free_quantity = models.PositiveIntegerField(default=0)
    is_optional = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)