from django.core.management.base import BaseCommand
from users.models.typology import Typology
from users.models.users import User 
from django.contrib.auth.hashers import make_password
from users.models.api_url import ApiUrl
from users.models.typology_api_url import TypologyApiUrl

class Command(BaseCommand):
    help = "Seed db with initial permissions"
    
    def handle(self, *args, **options):
        
        #typologies seeders
        Typology.objects.get_or_create(
            typology_name = "Admin"
        )
        
        Typology.objects.get_or_create(
            typology_name = "Restaurant Admin"
        )
        
        Typology.objects.get_or_create(
            typology_name = "Dealer"
        )
        
        Typology.objects.get_or_create(
            typology_name = "Customer"
        )
        
        # api url seeders
        
        # users
        ApiUrl.objects.get_or_create(
            name="Crear Usuario",
            url="/api/users/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de usuarios",
            url="/api/users/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Eliminar usuario por id",
            url="/api/users/delete/{pk}",
            method="DELETE"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener usuario por id",
            url="/api/users/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar usuario",
            url="/api/users/update/{pk}",
            method="PUT"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar contraseña de usuario",
            url="/api/users/reset_password/",
            method="PATCH"
        )
        
        #typologies
        ApiUrl.objects.get_or_create(
            name="Crear tipologia",
            url="/api/typologies/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de tipologias",
            url="/api/typologies/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener tipologia por id",
            url="/api/typologies/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar tipologia",
            url="/api/typologies/update/{pk}",
            method="PUT"
        )
        
        # ApiUrl.objects.get_or_create(
        #     name="Eliminar tipologia",
        #     name="/api/typologies/delete/{pk}",
        #     method="DELETE"
        # )
        
        #apiurls
        ApiUrl.objects.get_or_create(
            name="Crear api url",
            url="/api/apiurl/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de urls",
            url="/api/apiurl/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener url por id",
            url="/api/apiurl/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar url",
            url="/api/apiurl/update/{pk}",
            method="PUT"
        )
        
        ApiUrl.objects.get_or_create(
            name="Eliminar url",
            url="/api/apiurl/delete/{pk}",
            method="DELETE"
        )
        
        # typology_api_urls
        ApiUrl.objects.get_or_create(
            name="Asignar permisos a una tipologia",
            url="/api/typology/apiurl/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Ver listado de permisos",
            url="/api/typology/apiurl/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Ver permiso por id",
            url="/api/typology/apiurl/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Eliminar permiso de una tipologia",
            url="/api/typology/apiurl/delete/{pk}",
            method="DELETE"
        )
        
        #restaurants
        ApiUrl.objects.get_or_create(
            name="Crear restaurante",
            url="/api/restaurants/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de restaurantes",
            url="/api/restaurants/list",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener restaurante",
            url="/api/restaurants/find/{pk}",
            method="GET"
        )
        
        #23
        ApiUrl.objects.get_or_create(
            name="Actualizar restaurante",
            url="/api/restaurants/update/{pk}",
            method="PUT"
        )
        
        ApiUrl.objects.get_or_create(
            name="Crear categoria de menu",
            url="/api/menu/categories/",
            method="POST"
        )
        
        # menu category
        ApiUrl.objects.get_or_create(
            name="Obtener listado de categorias de menu",
            url="/api/menu/categories/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener menu de categoria por id",
            url="/api/menu/categories/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar categoria de menu",
            url="/api/menu/categories/update/{pk}",
            method="PUT"
        )
        
        #28
        ApiUrl.objects.get_or_create(
            name="Crear menu item",
            url="/api/menuitems/",
            method="POST"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de menu items",
            url="/api/menuitems/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener item por id",
            url="/api/menuitems/find/{pk}",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Actualizar item",
            url="/api/menuitems/update/{pk}",
            method="GET"
        )
        #32
        ApiUrl.objects.get_or_create(
            name="Crear orden",
            url="/api/orders/",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Cronsultar listado de ordenes del restaurante",
            url="/api/orders/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Cronsultar listado de ordenes (repartidor)",
            url="/api/orders/dealer/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Obtener listado de menu items de un restaurante para el cliente",
            url="/api/menuitems/list/{pk}",
            method="GET"
        )
        #36
        ApiUrl.objects.get_or_create(
            name="Obtener listado de ordenes del cliente",
            url="/api/orders/customer/list",
            method="GET"
        )
        
        ApiUrl.objects.get_or_create(
            name="Pasar una orden a estado 'En camino'",
            url="/api/orders/{pk}/progress",
            method="PATCH"
        )
        
        ApiUrl.objects.get_or_create(
            name="Pasar una orden a estado 'Entregado'",
            url="/api/orders/{pk}/delivered",
            method="PATCH"
        )
        
        ApiUrl.objects.get_or_create(
            name="Pasar una orden a estado 'Cancelado'",
            url="/api/orders/{pk}/cancel",
            method="PATCH"
        )
        
        # asign permissions
        for i in range(1, 23):
            TypologyApiUrl.objects.get_or_create(
                typology_id = 1,
                api_url_id = i
            )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 23
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 24
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 25
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 26
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 27
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 28
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 29
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 30
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 31
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 32
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 33
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 34
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 32
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 35
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 36
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 1
        )
        # TypologyApiUrl.objects.get_or_create(
        #     typology_id = 2,
        #     api_url_id = 3
        # )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 4
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 5
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 6
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 22
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 1
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 6
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 5
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 21
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 20
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 1
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 3
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 37
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 37
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 38
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 3,
            api_url_id = 38
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 39
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 2,
            api_url_id = 39
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 4
        )
                
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 5
        )
                
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 6
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 21
        )
        
        TypologyApiUrl.objects.get_or_create(
            typology_id = 4,
            api_url_id = 20
        )
        
        User.objects.get_or_create(
            first_name =  "Test",
            last_name = "Admin",
            email = "admintest@gmail.com",
            password = make_password("Quick2024*"),
            phone = "344444444",
            address = "Transversal 93 # 51 - 98 Und. 24 -25",
            typology_id = 1,
        )
        
        # User.objects.get_or_create(
        #     first_name =  "Test",
        #     last_name = "Restaurant Admin",
        #     email = "resadmintest@gmail.com",
        #     password = make_password("Quick2024*"),
        #     phone = "34445555",
        #     address = "Transversal 93 # 51 - 98 Und. 24 -25",
        #     typology_id = 2,
        # )
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded dbs"))
        
    