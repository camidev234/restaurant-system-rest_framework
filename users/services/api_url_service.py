from rest_framework.exceptions import ValidationError, NotFound

from users.models.api_url import ApiUrl
from users.serializers.api_url_serializers import ApiUrlSaveSerializer, ApiUrlGetSerializer, ApiUrlUpdateSerializer

class ApiUrlService:
    
    def save(self, data):
        serializer = ApiUrlSaveSerializer(data=data)
        if serializer.is_valid():
            api_url_saved = serializer.save()
            api_url_serialized = ApiUrlSaveSerializer(api_url_saved)
            return api_url_serialized.data
        
        raise ValidationError(serializer.errors)
    
    def get_api_url_instance(self, pk):
        try:
            api_url_found = ApiUrl.objects.get(id=pk)
            return api_url_found
        except ApiUrl.DoesNotExist:
            raise NotFound("The api url does not exists")
        
    def get_by_id(self, id):
        api_url_found = self.get_api_url_instance(id)
        api_url_serialized = ApiUrlGetSerializer(api_url_found)
        return api_url_serialized.data
    
    def get_all_api_urls(self):
        api_urls = ApiUrl.objects.all().order_by('id')
        return api_urls
    
    def update_api_url(self, data, id):
        api_url_found = self.get_api_url_instance(id)
        serializer = ApiUrlUpdateSerializer(api_url_found, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data            
            
        raise ValidationError(serializer.errors)
        
        