from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    address = models.TextField()
    category = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=21, decimal_places=11, null=True, blank=True)
    longitude = models.DecimalField(max_digits=21, decimal_places=11, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now to save when the row is updated
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'restaurants'