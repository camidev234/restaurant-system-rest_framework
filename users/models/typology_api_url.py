from users.models import typology, api_url

from django.db import models

#many to many (N:N)

class TypologyApiUrl(models.Model):
    typology = models.ForeignKey(typology.Typology, on_delete=models.CASCADE)  
    api_url = models.ForeignKey(api_url.ApiUrl, on_delete=models.CASCADE)  
    
    class Meta:
        db_table = 'typology_api_urls'
        