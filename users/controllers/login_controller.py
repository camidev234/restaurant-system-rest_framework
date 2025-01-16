from rest_framework.views import APIView
from users.services.auth_service import AuthService
from restaurantsystem.utils.api_response import ApiSuccessResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class LoginController(APIView):
    
    permission_classes = [AllowAny]
    
    def __init__(self, auth_service=None):
        super().__init__()
        self.auth_service = auth_service or AuthService()
    
    def post(self, request):
        if request.method == "POST":
            data = self.auth_service.login(request.data)
            api_response = ApiSuccessResponse(200, data, "Login successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
            
            
            
            
        