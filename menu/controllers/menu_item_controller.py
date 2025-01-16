from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from restaurantsystem.utils.paginator import Paginator
from menu.services.menu_item_service import MenuItemService
from menu.serializers.menu_item_serializers import MenuItemGetSerializer

class MenuItemSaveController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, menu_item_service=None):
        super().__init__()
        self.menu_item_service = menu_item_service or MenuItemService()
        
    def post(self, request):
        menu_item_saved = self.menu_item_service.save(request)
        api_repsonse = ApiSuccessResponse(201, menu_item_saved, "Menu item created successfully")
        return Response(api_repsonse.get_response(), status=status.HTTP_201_CREATED)
    
class MenuItemGetController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, menu_item_service=None):
        super().__init__()
        self.menu_item_service = menu_item_service or MenuItemService()
        
    def get(self, request, pk):
        item = self.menu_item_service.get_item_by_id(pk)
        api_response = ApiSuccessResponse(200, item, "Menu item found sucessfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    
class MenuItemListController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, menu_item_service=None, paginator=None):
        super().__init__()
        self.menu_item_service = menu_item_service or MenuItemService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        try:
            self.paginator.validate_query_param(request)
            items = self.menu_item_service.get_all_items(request, True, None)
            paginated_items = self.paginator.paginate_query_set(items, request)
                
            serialized_items = MenuItemGetSerializer(paginated_items, many=True)
                
            paginator_object = self.paginator.get_paginator_object()
                
            return paginator_object.get_paginated_response(serialized_items.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
            
class MenuItemListCustomerController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, menu_item_service=None, paginator=None):
        super().__init__()
        self.menu_item_service = menu_item_service or MenuItemService()
        self.paginator = paginator or Paginator()
        
    def get(self, request, pk):
        try:
            self.paginator.validate_query_param(request)
            items = self.menu_item_service.get_all_items(request, False, pk)
            paginated_items = self.paginator.paginate_query_set(items, request)
                
            serialized_items = MenuItemGetSerializer(paginated_items, many=True)
                
            paginator_object = self.paginator.get_paginator_object()
                
            return paginator_object.get_paginated_response(serialized_items.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )

class MenuItemUpdateController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, menu_item_service=None):
        super().__init__()
        self.menu_item_service = menu_item_service or MenuItemService()
        
    def put(self, request, pk):
        item_updated = self.menu_item_service.update_by_id(pk, request.data)
        api_response = ApiSuccessResponse(200, item_updated, "Item updated Successfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)