from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]