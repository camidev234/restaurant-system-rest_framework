from rest_framework.views import APIView
from rest_framework.response import Response
from users.services.user_service import UserService
from rest_framework.pagination import PageNumberPagination
from users.serializers.user_serializers import UserGetSerializer
from rest_framework import status
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from restaurantsystem.utils.paginator import Paginator
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserSaveController(APIView):
    
    permission_classes = [AllowAny]
    
    def __init__(self, user_service=None):
        super().__init__()
        self.user_service = user_service or UserService()
        
    
    def post(self, request):
        if request.method == "POST":
            user_saved = self.user_service.save(request.data)
            response_data = ApiSuccessResponse(201, user_saved, "User created successfully")
            return Response(response_data.get_response(), status=status.HTTP_201_CREATED)
    
class UserListController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, user_service=None, paginator=None):
        super().__init__()
        self.user_service = user_service or UserService()
        self.paginator = paginator or Paginator()
    
    def get(self, request):
        try:
            # page_size = request.query_params.get("page_size", 10)
            # try:
            #     page_size = int(page_size)
            #     if page_size <= 0:
            #         raise ValueError("El tamaño de cada página debe ser mayor que 0")
            # except (ValueError, TypeError):
            #     error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            #     api_response = ApiErrorResponse(400, message=error)
            #     return Response(
            #         api_response.get_response(),
            #         status=status.HTTP_400_BAD_REQUEST
            #     )

            self.paginator.validate_query_param(request)
            
             # Si pasa la validación del parámetro
            users = self.user_service.get_all(request.user)

            # Crear paginador
            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # paginated_users = paginator.paginate_queryset(users, request)

            paginated_users = self.paginator.paginate_query_set(users, request)

            # print(paginated_users)
            users_serialized = UserGetSerializer(paginated_users, many=True)
            
            # print("segundo")
            # print(users_serialized.data)

            paginator_object = self.paginator.get_paginator_object() 
        
            return paginator_object.get_paginated_response(users_serialized.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
        
class UserDeleteController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, user_service=None):
        super().__init__()
        self.user_service = user_service or UserService()
        
    def delete(self, request, pk):
        if request.method == "DELETE":
            succes_delete = self.user_service.delete_by_id(pk)
            if succes_delete:
                api_response = ApiSuccessResponse(200, None, "User deleted successfully")
                return Response(api_response.get_response(), status=status.HTTP_200_OK)
            
class UserUpdateController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, user_service=None):
        super().__init__()
        self.user_service = user_service or UserService()
        
    def put(self, request, pk):
        if request.method == "PUT":
            user_data = request.data
            updated_user = self.user_service.update_user(pk, user_data)
            
            if updated_user:
                api_response = ApiSuccessResponse(200, updated_user, "User updated successfully")
                return Response(api_response.get_response(), status=status.HTTP_200_OK) 
            
class UserUpdatePasswordController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, user_service=None):
        super().__init__()
        self.user_service = user_service or UserService()
        
    def patch(self, request):
        if request.method == "PATCH":
            data = request.data
           
            updated_success = self.user_service.update_user_password(request.user, data)
            if updated_success:
                api_response = {
                    "status": 200,
                    "message": "Password updated successfully"
                }
                return Response(api_response, status=status.HTTP_200_OK)

class UserGetUserController(APIView):
    permission_classes = [IsAuthenticated]
    def __init__(self, user_service=None):
        super().__init__()
        self.user_service = user_service or UserService()
        
    def get(self, request, pk):
        if request.method == "GET":
            success, user = self.user_service.get_user_by_id(pk, request.user)
            if not success:
                api_response = ApiErrorResponse(
                    403, 
                    message="You cannot see information about a user who is in a different restaurant"
                )
                return Response(api_response.get_response(), status=status.HTTP_403_FORBIDDEN)
            
            api_response = ApiSuccessResponse(200,  user, "User found successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
            
            
    
            
            
            
            