from .api_response import ApiErrorResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

class Paginator:
    
    def __init__(self):
        self.page_size = 10
        self.paginator_object = PageNumberPagination()
        
    def validate_query_param(self, request):
        
        page_size = request.query_params.get("page_size", 10)
        
        page_size = int(page_size)
        self.page_size = page_size
        if page_size <= 0:
            raise ValueError("El tamaño de cad pagina debe ser mayor que 0")
    

    def paginate_query_set(self, query_set, request):
        paginator = self.paginator_object
        paginator.page_size = self.page_size
        paginated_users = paginator.paginate_queryset(query_set, request)
        
        return paginated_users
    
    def get_paginator_object(self):
        return self.paginator_object