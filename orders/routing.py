from django.urls import re_path
from orders.consumers import order_consumer

websocket_urlpatterns = [
    re_path(r"^ws/orders/(?P<order_id>\d+)/$", order_consumer.OrderConsumer.as_asgi()),
]