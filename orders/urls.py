from django.urls import path
from orders.controllers.order_controller import OrderSaveController, OrderGetController, OrderListController, OrderListCustomerOrders, OrderListAssignedDealerController

urlpatterns = [
    path('orders/', OrderSaveController.as_view(), name="save_order"),
    path('orders/find/<int:pk>', OrderGetController.as_view(), name="order_find"),
    path('orders/list', OrderListController.as_view(), name="list_orders"),
    path('orders/customer/list', OrderListCustomerOrders.as_view(), name="customer_order_list"),
    path('orders/dealer/list', OrderListAssignedDealerController.as_view(), name="dealer_orders_list")
]