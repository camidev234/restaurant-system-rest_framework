from rest_framework import serializers
from users.models.typology_api_url import TypologyApiUrl

from users.models.typology import Typology

class TypologyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typology
        fields = ['id', 'typology_name', 'active', 'created_at']

class TypologySerializer(serializers.ModelSerializer):
    
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Typology
        fields = ['id', 'typology_name', 'active', 'created_at', 'permissions']
        
    def get_permissions(self, obj):
        
        permissions = TypologyApiUrl.objects.filter(typology=obj)
        return [
            {
                "permission_id": permission.id,
                "name": permission.api_url.name,
                "url": permission.api_url.url
                
            }
            for permission in permissions
        ]
        
class TypologySaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typology
        fields = ['id', 'typology_name']


class TypologyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Typology
        fields = ['id', 'typology_name']
