from rest_framework.views import APIView
from restaurantsystem.utils.api_response import ApiSuccessResponse, ApiErrorResponse
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.response import Response
from rest_framework import status 
from orders.services.order_service import OrderService
from restaurantsystem.utils.paginator import Paginator
from orders.serializers.order_serializers import OrderGetSerializer

class OrderSaveController(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        
    def post(self, request):
        success, result = self.order_service.save(request.data, request.user)
        if success:
            api_response = ApiSuccessResponse(201, result, "Orden creada correctamente")
            return Response(api_response.get_response(), status=status.HTTP_201_CREATED)
        else:
            api_response = ApiErrorResponse(400, result, "An error ocurred")
            return Response(api_response.get_response(), status=status.HTTP_400_BAD_REQUEST)
        
        
class OrderGetController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        
    def get(self, request, pk):
        order_found = self.order_service.get_order_by_id(pk)
        api_response = ApiSuccessResponse(200, order_found, "Order found successfully")
        return Response(api_response.get_response(), status=status.HTTP_200_OK)
    

class OrderListController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None, paginator=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        try:
            self.paginator.validate_query_param(request)
            orders = self.order_service.get_restaurant_orders(request.user)
            paginated_orders = self.paginator.paginate_query_set(orders, request)
            
            serialized_orders = OrderGetSerializer(paginated_orders, many=True)
            
            paginator_object = self.paginator.get_paginator_object()
            
            return paginator_object.get_paginated_response(serialized_orders.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
            
class OrderListAssignedDealerController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None, paginator=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        try:
            self.paginator.validate_query_param(request)
            orders = self.order_service.get_user_orders(request.user, True)
            
            paginated_orders = self.paginator.paginate_query_set(orders, request)
            
            serialized_orders = OrderGetSerializer(paginated_orders, many=True)
            
            paginator_object = self.paginator.get_paginator_object()
            
            return paginator_object.get_paginated_response(serialized_orders.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
            
class OrderListCustomerOrders(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None, paginator=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        self.paginator = paginator or Paginator()
        
    def get(self, request):
        try:
            self.paginator.validate_query_param(request)
            orders = self.order_service.get_user_orders(request.user, False)
            
            paginated_orders = self.paginator.paginate_query_set(orders, request)
            
            serialized_orders = OrderGetSerializer(paginated_orders, many=True)
            
            paginator_object = self.paginator.get_paginator_object()
            
            return paginator_object.get_paginated_response(serialized_orders.data)
        except (ValueError, TypeError):
            error = {"error": "El parámetro 'page_size' debe ser un número válido"}   
            api_response = ApiErrorResponse(400, message=error)
            return Response(
                api_response.get_response(),
                status=status.HTTP_400_BAD_REQUEST
            )
            
class OrderAssignController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        
    def patch(self, request, pk):
        result = self.order_service.assign_order(request.data, pk)
        
        if result:
            api_response = ApiSuccessResponse(200, None, "Order assigned successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
        
        api_response = ApiErrorResponse(400, None, "An error ocurred, maybe the order cannot be assigned")
        return Response(api_response.get_response(),status=status.HTTP_400_BAD_REQUEST)
        
class OrderDeliverController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        
    def patch(self, request, pk):
        result = self.order_service.deliver_order(pk, request.user)
        
        if result:
            api_response = ApiSuccessResponse(200, None, "Order Devlivered successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
        
class OrderPayController(APIView):
    permission_classes = [IsAuthenticated]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
        
    def post(self, request):
        (success, data) = self.order_service.create_order_payment(request.data) 
        if success:
            api_response = ApiSuccessResponse(200, data, "Order payed sucessfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
        
        api_response = ApiErrorResponse(400, None, data.get("error"))
        return Response(api_response.get_response(), status=status.HTTP_400_BAD_REQUEST)
    
class OrderWebhookController(APIView):
    permission_classes = [AllowAny]
    
    def __init__(self, order_service=None):
        super().__init__()
        self.order_service = order_service or OrderService()
    
    def post(self, request):
        print("WEBHOOK RECIBIDO")
        print(request.data)
        result = self.order_service.receive_payment_webhook(
            request.data["type"], 
            request.data["transaction"]["order_id"]
        )
        
        if result:
            api_response = ApiSuccessResponse(200, None, "Webhook received and porcessed successfully")
            return Response(api_response.get_response(), status=status.HTTP_200_OK)
        
        api_response = ApiErrorResponse(501, None, "The webhook cannot be processed")
        return Response(api_response.get_response(), status=status.HTTP_501_NOT_IMPLEMENTED)
    
        