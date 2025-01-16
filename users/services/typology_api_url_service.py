from rest_framework.exceptions import ValidationError, NotFound
from users.serializers.typology_api_url_serializers import TypologyApiUrlSaveSerializer, TypologyApiUrlInvalidSerializer
from users.models.api_url import ApiUrl
from users.models.typology_api_url import TypologyApiUrl
from django.db import transaction

class TypologyApiUrlService:
    def save(self, data):
        serializer = TypologyApiUrlSaveSerializer(data=data)
        if serializer.is_valid():
            typology_id = data.get('typology_id')
            api_url_ids = data.get('api_url_ids', [])
            
            invalid_ids = []
            # validate if all id's (table api_url) exists
            for api_url_id in api_url_ids:
                if not ApiUrl.objects.filter(id=api_url_id).exists():
                    invalid_ids.append(api_url_id)
                    
            # if some id does not exists
            if len(invalid_ids) > 0:
                data_object = {
                    "reason": "The list of id's contains non-existent api_url",
                    "invalid_ids": invalid_ids
                }
                
                serializer_invalid_ids = TypologyApiUrlInvalidSerializer(data_object)
                return False, serializer_invalid_ids.data
            
            try:
                with transaction.atomic():
                    created_count = 0
                    for api_url_id in api_url_ids:
                        # validate if relation exists
                        if not TypologyApiUrl.objects.filter(typology_id=typology_id, api_url_id=api_url_id).exists():
                            # if not exists, create a permission
                            # else continue
                            TypologyApiUrl.objects.create(
                                typology_id=typology_id,
                                api_url_id=api_url_id
                            )
                            created_count+=1
                    
                    data_object = {
                        "created": created_count
                    }
                    
                    return True, data_object
            except Exception as e:
                pass
        
        raise ValidationError(serializer.errors)
    
    def get_typology_permission_instance(self, id):
        try:
            permission_group = TypologyApiUrl.objects.get(id=id)
            return permission_group
        except TypologyApiUrl.DoesNotExist:
            raise NotFound("The user doesn't found")
        
    def delete_by_id(self, permission_id):
        permission_to_delete = self.get_typology_permission_instance(permission_id)
        permission_to_delete.delete()
        return True