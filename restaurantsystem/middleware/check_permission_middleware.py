from rest_framework.response import Response
from rest_framework import status
from users.models import typology_api_url
from rest_framework.permissions import AllowAny
from django.http import JsonResponse
import re

class CheckPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        actual_url = request.path
        
        response = self.get_response(request)

        if self._has_allow_any_permission(request):
            return response

        typology_id = None
        if request.user.is_authenticated:
            typology_id = request.user.typology.id
        else:
            return JsonResponse({"message": "Your token is expired or invalid"}, status=401)

        permissions = typology_api_url.TypologyApiUrl.objects.filter(typology_id=typology_id)
        message = f"Users of typology [{request.user.typology.typology_name}] are not allowed access to this resource"
        has_permission = False

        if not permissions:
            
            return JsonResponse({
                "message": message,
            }, status=403)
        # print("url actual: ", actual_url)
        
        view_kwargs = request.resolver_match.kwargs
        print("Parametros de la URL:", view_kwargs)

        pk_value = view_kwargs.get('pk', None)

        for permission in permissions:
            api_url = permission.api_url.url # /api/typology/apiurl/delete/{pk}
            if pk_value is not None:
                api_url = api_url.replace("{pk}", str(pk_value))
            
            if api_url == actual_url:
                has_permission = True
                break

        if not has_permission:
            return JsonResponse({
                "message": message,
            }, status=401)

        return response

    def _has_allow_any_permission(self, request):
        if hasattr(request, 'resolver_match') and request.resolver_match:
            view = request.resolver_match.func.cls if hasattr(request.resolver_match.func, 'cls') else None
            if view:
                permissions = getattr(view, 'permission_classes', [])
                return any(isinstance(permission(), AllowAny) for permission in permissions)
        return False
