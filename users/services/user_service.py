from users.serializers.user_serializers import UserSerializer, UserGetSerializer, UserUpdateSerializer, UserUpdatePasswordSerializer
from rest_framework.exceptions import ValidationError, NotFound
from users.models.users import User
from django.contrib.auth.hashers import make_password

class UserService:

    def save(self, user_data):
        if 'password' in user_data:
            user_data['password'] = make_password(user_data['password'])
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            user_saved = serializer.save()
            user_serialized = UserSerializer(user_saved)
            return user_serialized.data
        
        raise ValidationError(serializer.errors)
    
    def get_all(self, user_auth):
        if user_auth.restaurant != None:
            users = User.objects.filter(restaurant=user_auth.restaurant).order_by('id')
        else: 
            users = User.objects.all().order_by('id')
        # users_serialized = UserGetSerializer(users, many=True)
        
        return users
    
    def get_user_instance(self, user_id):
        try:
            user_found = User.objects.get(id=user_id)
            return user_found
        except User.DoesNotExist:
            raise NotFound("The user doesn't found")
        
    def delete_by_id(self, user_id):
        user_to_delete = self.get_user_instance(user_id)
        user_to_delete.delete()
        return True
    
    def update_user(self, user_id, user_data):
        user_to_update = self.get_user_instance(user_id)
        serializer = UserUpdateSerializer(user_to_update, data=user_data)
        
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        
        raise ValidationError(serializer.errors)
    
    def update_user_password(self, user, data):
        # print("gggg")
        
        if 'password' in data:
            data['password'] = make_password(data['password'])
            
        serializer = UserUpdatePasswordSerializer(user, data=data, partial=True) 
        
        if serializer.is_valid():   
            serializer.save()
            return True
        
        raise ValidationError(serializer.errors)
    
    def get_user_by_id(self, pk, user_auth):
        user_found = self.get_user_instance(pk)
        if user_found.restaurant != user_auth.restaurant:
            if user_auth.restaurant == None:
                user_serialized = UserGetSerializer(user_found)
            else:
                return False, None
                    
        user_serialized = UserGetSerializer(user_found)
        
        return True, user_serialized.data