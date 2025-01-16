from rest_framework import serializers

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=8)
    password = serializers.CharField(required=True)
    
    # def validate_email(self, value):
    #     if not value or "@" not in value:
            