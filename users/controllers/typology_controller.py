from rest_framework.views import APIView
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from rest_framework.permissions import AllowAny, IsAuthenticated 
from users.services.typology_service import TypologyService
from rest_framework.response import Response
from rest_framework import status 
from restaurantsystem.utils.paginator import Paginator
from users.serializers.typology_serializers import TypologySerializer

class TypologySaveController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_service=None):
        super().__init__()
        self.typology_service = typology_service or TypologyService()
        
    
    def post(self, request):
        if request.method == "POST":
            typology_saved = self.typology_service.save(request.data)
            api_response = ApiSuccessResponse(201, typology_saved, "Typology created successfully")
            return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
        
class TypologyListController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_service=None, paginator=None):
        super().__init__()
        self.typology_service = typology_service or TypologyService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        if request.method == "GET":
            try:
                self.paginator.validate_query_param(request)
                typologies = self.typology_service.get_all_typologies()
                paginated_typologies = self.paginator.paginate_query_set(typologies, request)
                
                serialized_typologies = TypologySerializer(paginated_typologies, many=True)
                
                paginator_object = self.paginator.get_paginator_object()
                
                return paginator_object.get_paginated_response(serialized_typologies.data)
            except (ValueError, TypeError):
                error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
                api_response = ApiErrorResponse(400, message=error)
                return Response(
                    api_response.get_response(),
                    status=status.HTTP_400_BAD_REQUEST
                )
                
class TypologyGetController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_service=None, paginator=None):
        super().__init__()
        self.typology_service = typology_service or TypologyService()
        
        
    def get(self, request, pk):
        if request.method == "GET":
            typology_found = self.typology_service.get_typology_by_id(pk)
            api_response = ApiSuccessResponse(200, typology_found, "Typology found successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)

class TypologyUpdateController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, typology_service=None, paginator=None):
        super().__init__()
        self.typology_service = typology_service or TypologyService()
        
    def put(self, request, pk):
        if request.method == "PUT":
            updated_typology = self.typology_service.update_typology(request.data, pk)
            if updated_typology:
                api_response = ApiSuccessResponse(200, updated_typology, "Typology updated successfully")
                return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
            
        