from orders.serializers.order_serializers import OrderSaveSerializer, OrderInvalidSerializer, OrderPaySerializer, OrderPayedSerializer, OrderAssignSerializer, OrderSerializer, OrderGetSerializer
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from menu.models.menu_item import MenuItem
from orders.serializers.order_item_serializers import OrderItemGetSerializer
from django.db import transaction
from orders.models.order_item import OrderItem
from orders.models.order import Order
from users.models.users import User
from orders.socket_services.order_web_socket_service import OrderWebSocketService
from asgiref.sync import async_to_sync
from orders.services.http_services.http_services import HttpServices 
from orders.models.payment_orders import PaymentOrder
from orders.services.payment_order_service import PaymentOrderService
from django.db import transaction
from orders.services.webhooks.webhook_payment_handler import WebhookPaymentHandler
from webhooks.services.webhook_service import WebhookService

class OrderService:
    
    def __init__(self, order_socket_service=None, payment_order_service=None, webhook_payment_handler=None, webhook_service=None):
        self.order_socket_service = order_socket_service or OrderWebSocketService()
        self.payment_order_service = payment_order_service or PaymentOrderService()
        self.webhook_payment_handler = webhook_payment_handler or WebhookPaymentHandler()
        self.webhook_service = webhook_service or WebhookService()
        
    def create_order_payment(self, request_data):
        serializer = OrderPaySerializer(data=request_data)
        
        if serializer.is_valid():
            order = self.__get_order_instance(request_data["order_id"])
            print(order.status.id)
            if order.status.id != 5:
                return (False, {
                    "error": "The order has already been paid"
                })
            payment_order = self.payment_order_service.save_payment_order(order)
            response_obj = HttpServices.pay_order_request(order, payment_order.order_gateway_id)
            
            if response_obj.get("pse_url"):
                response = OrderPayedSerializer(response_obj)
                self.payment_order_service.assign_order_transaction(
                    payment_order, 
                    response_obj.get("transaction_id")
                )
                
                return (True, response.data)

            return (False, response_obj)  
        
        raise ValidationError(serializer.errors)   
           
           
    def receive_payment_webhook(self, data):
        
        type = data["type"]
        match type:
            case "charge.succeeded":
                order_gateway_id = data["transaction"]["order_id"]
                result = self.webhook_payment_handler.handle_charge_succeeded(
                    order_gateway_id,
                    self.payment_order_service,
                )
                self.webhook_service.receive_message(data)
                
                return result
            case "charge.cancelled":
                order_gateway_id = data["transaction"]["order_id"]
                result = self.webhook_payment_handler.handle_charge_cancelled(
                    order_gateway_id, 
                    self.payment_order_service
                )
                self.webhook_service.receive_message(data)
                
                return result
            case "charge.failed":
                order_gateway_id = data["transaction"]["order_id"]
                result = self.webhook_payment_handler.handle_charge_failed(
                    order_gateway_id,
                    self.payment_order_service
                )
                self.webhook_service.receive_message(data)
                return result
            case "verification":
                result = self.webhook_service.receive_message(data)
                return result
                

    def save(self, data, user_auth):
        serializer = OrderSaveSerializer(data=data)
        if serializer.is_valid():
            # se obtiene los items del serializer, estos se pasaron en la key 'order_items'
            order_items = serializer.validated_data['order_items']
            invalid_items = []
            total_amount = 0

            for order_item in order_items:
                # consulta para obtener menu item donde el id sea igual al de la iteracion actual y este activo
                menu_item = MenuItem.objects.filter(id=order_item['id'], active=True).first()
                # si no se encontro el menu item
                if not menu_item:
                    # se agrega el item que no se encontro a la lista de items invalidos
                    invalid_items.append(order_item['id'])
                else:
                    # si si se encontro, la variable item total guarda el total del item multiplicado por el quantity
                    # menu_item.price = 44.500 * order_item['quantity]=2 = 89.000
                    item_total = menu_item.price * order_item['quantity']
                    total_amount += item_total

            # si hay items invalidos
            if len(invalid_items) > 0:
                data_object = {
                    "reason": "Some items are invalid or inactive.",
                    "invalid_items": invalid_items
                }
                # se serializa el objeto usando el OrderInvalidSerializer
                serializer_invalid_items = OrderInvalidSerializer(data_object)
                return False, serializer_invalid_items.data

            try:
                order_data = serializer.validated_data
                # a la data de la orden a crear, se le crea una key llamada 'total_amount' y se le asigna el valor de la varuable total_amount
                # lo mismo para customer id, solo que se le asigna el id del usuario autenticado
                order_data['total_amount'] = total_amount
                order_data['customer_id'] = user_auth.id

                with transaction.atomic():
                    
                    # se pasa el estado de la orden a id 5 "Pendiente por pago"
                                        
                    order_saved = serializer.save() 
                    

                    # se serializa el order guardado usando el OrderSerializer
                    order_serializer = OrderSerializer(order_saved)
                    # se obtienen los order items relacionados a la orden recien guardado
                    # esto teniendo en cuenta que el serializer OrderSaveSerializer contiene una fucion create
                    # la funcion create se encarga de recorrer los order_items que estan en la data del serializer e irlos guardando
                    order_items_details = OrderItem.objects.filter(order=order_saved)
                    menu_items = []
                    # se recorren los order items de la order guardada para agregarlos a una lista, cada elemento incluira el detalle del order item
                    for order_item in order_items_details:
                        menu_item_data = {
                            'id': order_item.menu_item.id,
                            'name': order_item.menu_item.name,
                            'price': str(order_item.menu_item.price),
                            'quantity': order_item.quantity
                        }
                        menu_items.append(menu_item_data)

                    return True, {
                        "order": order_serializer.data,
                        "order_items": menu_items
                    }

            except Exception as e:
                print(e)

        raise ValidationError(serializer.errors)
    
    
    def __get_order_instance(self, id):
        try:
            order = Order.objects.get(id=id)
            return order
        except Order.DoesNotExist:
            raise NotFound("The order does not exists")
    
    
    def __get_order_items(self, order_obj):
        order_items = order_obj.order_items.all()
        
        order_menu_items = []
        
        'id', 'menu_item_id', 'item_name', 'description', 'price', 'category_name', 'image_url', 'quantity', 'active', 'created'
        
        for order_item in order_items:
            obj = {
                "id": order_item.id,
                "menu_item_id": order_item.menu_item.id,
                "item_name": order_item.menu_item.name,
                "description": order_item.menu_item.description,
                "price": order_item.menu_item.price,
                "category_name": order_item.menu_item.category.category_name,
                "image_url": order_item.menu_item.image_url,
                "quantity": order_item.quantity,
                "active": order_item.active,
                "created": order_item.created
            }
            
            order_menu_items.append(obj)
        
        return order_menu_items
    
    def get_order_by_id(self, pk):
        # obtiene la orden por id
        order_found = self.__get_order_instance(pk)
        # serializa los items de la ordern, y se asigna la data ya serializada
        order_found_items = OrderItemGetSerializer(self.__get_order_items(order_found), many=True).data
        # serializa el orderGetSerializer, aca solo se incluirian datos de el Order y se asigna la data
        order_get_serializer =  OrderGetSerializer(order_found).data
        # dinamicamente se agrega una key order_items a la data de Order que incluye los items de la orden serializados
        order_get_serializer["order_items"] = order_found_items
        return order_get_serializer
    
    def get_restaurant_orders(self, user_auth):
        if not user_auth.restaurant:
            raise PermissionDenied("You dont have access to this orders list")
        
        orders = Order.objects.filter(restaurant_id = user_auth.restaurant.id)
        return orders.order_by('id')
    
    def get_user_orders(self, user_auth, is_dealer):
        if not is_dealer:
            orders = Order.objects.filter(customer_id = user_auth.id)
        else:
            orders = Order.objects.filter(dealer_id = user_auth.id) 
        
        return orders
    
    def assign_order(self, data, order_id):
        serializer = OrderAssignSerializer(data=data)
        
        if serializer.is_valid():
            order = self.__get_order_instance(order_id)
            dealer = User.objects.get(id=data["dealer_id"])
            order.dealer = dealer
            
            match order.status_id:
                case 1:
                    order.status_id = 2  
                    order.save() 
                case 2:
                    order.save()
                case 3:
                    return False
                case 4: 
                    return False
                case 5:
                    return False

            if dealer.restaurant != order.restaurant:
                raise PermissionDenied("The delivery person must belong to the same restaurant as the order")

            # función asíncrona de WebSocket de manera síncrona
            async_to_sync(self.order_socket_service.send_order_update)(order.id, order.status.id, order.status.status_name)
            async_to_sync(self.order_socket_service.send_order_list_restaurant_update)(order.id, order.status.id, order.restaurant.id,  order.status.status_name)
            
            return True
        
        raise ValidationError(serializer.errors)
    
    
    def deliver_order(self, order_id, user_auth):
        order = self.__get_order_instance(order_id)
        
        if user_auth.restaurant.id != order.restaurant.id:
            raise PermissionDenied("Only people from the same restaurant can deliver an order") 

        if order.status_id == 5 or order.status_id == 4:
            return False
        
        order.status_id = 3
        order.save()

        async_to_sync(self.order_socket_service.send_order_update)(order.id, order.status.id, order.status.status_name)
        async_to_sync(self.order_socket_service.send_order_list_restaurant_update)(order.id, order.status.id, order.restaurant.id,  order.status.status_name)
        
        return True
    
    def cancel_order(self):
        pass
        
        
        
        
        
        
        
        
        
        
        