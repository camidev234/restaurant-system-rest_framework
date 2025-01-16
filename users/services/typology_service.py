from users.serializers.typology_serializers import TypologySaveSerializer, TypologySerializer, TypologyUpdateSerializer
from rest_framework.exceptions import ValidationError
from users.models.typology import Typology
from rest_framework.exceptions import NotFound

class TypologyService:
    def save(self, data):
        serializer = TypologySaveSerializer(data=data)
        if serializer.is_valid():
            typology_saved = serializer.save()
            typology_serialized = TypologySaveSerializer(typology_saved)
            return typology_serialized.data
        
        raise ValidationError(serializer.errors)
    
    def get_all_typologies(self):
        typologies = Typology.objects.all().order_by('id')
        return typologies
    
    
    def get_typlogy_instance(self, id):
        try:
            typology_found = Typology.objects.get(id=id)
            return typology_found
        except Typology.DoesNotExist:
            raise NotFound("The typology does not exists")
    
    def get_typology_by_id(self, id):
        typology_found = self.get_typlogy_instance(id)
        
        typology_serialized = TypologySerializer(typology_found)
        
        return typology_serialized.data
    
    def update_typology(self, data, id):
        typology_to_update = self.get_typlogy_instance(id)
        serializer = TypologyUpdateSerializer(typology_to_update, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        
        raise ValidationError(serializer.errors)
        