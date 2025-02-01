from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from asgiref.sync import sync_to_async

from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from asgiref.sync import sync_to_async
from django.conf import settings
from users.models import User

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        token = self.get_token_from_headers(scope)
        # si el token no es None de acuerdo a lo que retorna el metodo anterior
        if token:
            try:
                # print("entra al middle")
                UntypedToken(token)
                # variable que almacena los claims del token suministrado (payload)                
                payload = UntypedToken(token).payload
                # se busca el usuario obteniendo el user_id de los claims
                user = await self.get_user(payload.get("user_id"))
                # se asigna al user del scope del socket, el usuario encontrado
                print("usuario", user)
                scope["user"] = user
            except (InvalidToken, TokenError) as e:
                # en caso de que al ejecutar UntypedToken, genera alguno de estos dos excepciones
                print(f"Token inválido o error: {e}")
                scope["user"] = AnonymousUser()
            except Exception as e:
                # escepcion generica
                print(f"Error inesperado al procesar el token JWT: {e}")
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    def get_token_from_headers(self, scope):
        # esta funcion obtiene el token de los headers
        headers = dict(scope.get('headers', []))
        auth_header = headers.get(b'authorization', None)
        if auth_header:
            parts = auth_header.decode().split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                return parts[1]
        return None

    @sync_to_async
    def get_user(self, user_id):
        from users.models import User
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()