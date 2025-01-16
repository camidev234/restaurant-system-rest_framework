from rest_framework import serializers
from users.models.api_url import ApiUrl

class ApiUrlSaveSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ApiUrl
        fields = ['id', 'name', 'url', 'method']
        
class ApiUrlGetSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField(read_only=True)
    url = serializers.CharField(read_only=True)
    method = serializers.CharField(read_only=True)
    
    class Meta:
        model = ApiUrl
        fields = ['id', 'name', 'url', 'method']
        
class ApiUrlUpdateSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = ApiUrl
        fields = ['id', 'name', 'url', 'method']