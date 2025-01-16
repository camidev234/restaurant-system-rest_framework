from django.db import models

class ApiUrl(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=200, unique=True) 
    method = models.CharField(max_length=10) 
    
    class Meta: 
        db_table = 'api_urls'