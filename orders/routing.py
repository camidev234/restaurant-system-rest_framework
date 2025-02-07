from django.urls import re_path
from orders.consumers import order_consumer, order_list_consumer, payment_consumer

websocket_urlpatterns = [
    re_path(r"^ws/orders/(?P<order_id>\d+)/$", order_consumer.OrderConsumer.as_asgi()),
    re_path(r"^ws/orders/restaurant/", order_list_consumer.OrderListConsumer.as_asgi()),
    re_path(r"^ws/orders/payment/(?P<payment_order_id>\w+)/$", payment_consumer.PaymentConsumer.as_asgi())
]