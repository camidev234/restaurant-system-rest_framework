from rest_framework.views import APIView
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status 
from users.services.api_url_service import ApiUrlService
from restaurantsystem.utils.paginator import Paginator
from users.serializers.api_url_serializers import ApiUrlGetSerializer

class ApiUrlSaveController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, api_url_service=None):
        super().__init__()
        self.api_url_service = api_url_service or ApiUrlService()
    
    def post(self, request):
        api_url_created = self.api_url_service.save(request.data)
        api_response = ApiSuccessResponse(201, api_url_created, "Api url created successfully")
        return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
        
        
class ApiUrlGetController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, api_url_service=None):
        super().__init__()
        self.api_url_service = api_url_service or ApiUrlService()
        
    def get(self, request, pk):
        api_url_found = self.api_url_service.get_by_id(pk)
        api_response = ApiSuccessResponse(200, api_url_found, "Api url found successfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
        
        
class ApiUrlListController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, api_url_service=None, pagimator = None):
        super().__init__()
        self.api_url_service = api_url_service or ApiUrlService()
        self.paginator = pagimator or Paginator()
        
    def get(self, request):
        try:
            self.paginator.validate_query_param(request)
            api_urls = self.api_url_service.get_all_api_urls()
            paginated_urls = self.paginator.paginate_query_set(api_urls, request)
            serialized_api_urls = ApiUrlGetSerializer(paginated_urls, many=True)
            paginator_object = self.paginator.get_paginator_object()
            return paginator_object.get_paginated_response(serialized_api_urls.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
                
class ApiUrlUpdateController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, api_url_service=None):
        super().__init__()
        self.api_url_service = api_url_service or ApiUrlService()
        
    def put(self, request, pk):
        api_url_updated = self.api_url_service.update_api_url(request.data, pk)
        api_response = ApiSuccessResponse(200, api_url_updated, "Api url updated successfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
        