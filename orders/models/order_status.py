from django.db import models

class OrderStatus(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    status_name = models.CharField(max_length=20)
    
    class Meta:
        db_table = "order_status"