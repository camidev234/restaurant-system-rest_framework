from users.serializers.auth_serializer import UserLoginSerializer
from users.serializers.user_serializers import UserGetSerializer
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from users.models.users import User
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class AuthService():
    def login(self, data):
        serializer = UserLoginSerializer(data=data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
        
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise AuthenticationFailed("User not found")
            
            if not check_password(password, user.password):
                raise AuthenticationFailed("Incorrect password")
            
            if not user.active:
                raise AuthenticationFailed("The user is not active")
            
            refresh = RefreshToken.for_user(user)
            
            user_detail = UserGetSerializer(user).data
            
            response_object = {
                "access_token": str(refresh.access_token),
                "refresh": str(refresh),
                "user": user_detail
            }
            
            return response_object
            
        raise ValidationError(serializer.errors)
        
        
        
        
    