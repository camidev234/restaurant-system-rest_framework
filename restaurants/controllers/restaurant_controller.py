from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from restaurantsystem.utils.paginator import Paginator
from restaurants.services.restaurant_service import RestaurantService
from restaurants.serializers.restaurant_serializer import RestaurantGetSerializer



class RestaurantSaveController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def  __init__(self, restaurant_service=None):
        super().__init__()
        self.restaurant_service = restaurant_service or RestaurantService()
    
    def post(self, request):
        if request.method == "POST":
            restaurant_created = self.restaurant_service.save(request.data)
            api_response = ApiSuccessResponse(201, restaurant_created, "Restaurant created sucessfully")
            return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
        
class RestaurantListController(APIView):
    permission_classes = [IsAuthenticated]
    
    def  __init__(self, restaurant_service=None, paginator=None):
        super().__init__()
        self.restaurant_service = restaurant_service or RestaurantService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        if request.method == "GET":
            try:
                self.paginator.validate_query_param(request)
                restaurants = self.restaurant_service.get_all_restaurants()
                paginated_restaurants = self.paginator.paginate_query_set(restaurants, request)

                serialized_restaurants = RestaurantGetSerializer(paginated_restaurants, many=True)

                paginator_object = self.paginator.get_paginator_object()

                return paginator_object.get_paginated_response(serialized_restaurants.data)
            except (ValueError, TypeError):
                error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
                api_response = ApiErrorResponse(400, message=error)
                return Response(
                    api_response.get_response(),
                    status=status.HTTP_400_BAD_REQUEST
                )
                
class RestaurantGetController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def  __init__(self, restaurant_service=None):
        super().__init__()
        self.restaurant_service = restaurant_service or RestaurantService()
        
    def get(self, request, pk):
        if request.method == "GET":
            restaurant = self.restaurant_service.get_by_id(pk)
            api_response = ApiSuccessResponse(200, restaurant, "Restaurant found successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
        

class RestaurantUpdateController(APIView):
    permission_classes = [IsAuthenticated]
    
    def  __init__(self, restaurant_service=None):
        super().__init__()
        self.restaurant_service = restaurant_service or RestaurantService()
        
    def put(self, request, pk):
        restaurant_updated = self.restaurant_service.update_by_id(request.data, pk)
        api_response = ApiSuccessResponse(200, restaurant_updated, "Restaurant updated successfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
        