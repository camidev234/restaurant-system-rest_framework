from rest_framework.views import APIView
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status
from users.services.typology_api_url_service import TypologyApiUrlService 

class TypologyPermissionSaveController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_api_url_service=None):
        super().__init__()
        self.typology_api_url_service = typology_api_url_service or TypologyApiUrlService()
    
    def post(self, request):
        if request.method == "POST":
            success, result = self.typology_api_url_service.save(request.data)
            if success:
                api_response = ApiSuccessResponse(201, result, "Permisos asignados correctamente")
                return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
            else:
                api_response = ApiErrorResponse(400, result, "An error ocurred")
                return Response(api_response.get_response(), status=status.HTTP_400_BAD_REQUEST)
            
class TypologyPermissionRevokeController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_api_url_service=None):
        super().__init__()
        self.typology_api_url_service = typology_api_url_service or TypologyApiUrlService()
        
    def delete(self, request, pk):
        if request.method == "DELETE":
            result = self.typology_api_url_service.delete_by_id(pk)
            if result:
                api_response = ApiSuccessResponse(200, None, "Permission revoked successfully")
                return Response(api_response.get_response(), status=status.HTTP_200_OK)
                