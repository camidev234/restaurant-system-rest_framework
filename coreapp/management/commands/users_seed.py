from django.core.management.base import BaseCommand
from users.models.typology import Typology
from users.models.users import User 
from django.contrib.auth.hashers import make_password
from users.models.api_url import ApiUrl
from users.models.typology_api_url import TypologyApiUrl

class Command(BaseCommand):
    help = "Seed db with initial permissions"
    
    def handle(self, *args, **options):
    
        Typology.objects.get_or_create(
                typology_name = "Admin"
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

        ApiUrl.objects.get_or_create(
                name="Crear tipologia",
                url="/api/typologies/",
                method="POST"
        )

        TypologyApiUrl.objects.get_or_create(
                typology_id = 1,
                api_url_id = 1
        )

        self.stdout.write(self.style.SUCCESS("Successfully seeded dbs"))
