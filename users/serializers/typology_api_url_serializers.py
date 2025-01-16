from rest_framework import serializers
from users.models.typology_api_url import TypologyApiUrl
from users.models.typology import Typology
from users.models.api_url import ApiUrl

class TypologyApiUrlSaveSerializer(serializers.Serializer):
    typology_id = serializers.PrimaryKeyRelatedField(
        queryset=Typology.objects.all(),
        write_only=True,
        required=True
    )
    
    api_url_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )

    class Meta:
        fields = ['id','typology_id', 'api_url_ids']
        

class TypologyApiUrlInvalidSerializer(serializers.Serializer):
    
    reason = serializers.CharField()
    invalid_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )
    
    class Meta:
        fields = ['reason', 'invalid_ids']