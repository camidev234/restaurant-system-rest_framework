from django.core.management.base import BaseCommand
from orders.models import OrderStatus 

class Command(BaseCommand):
    help = "Seed db with initial permissions"

    def handle(self, *args, **options):
        statuses = ["Pendiente", "En camino", "Entregado", "Cancelado"]
        
        for status_name in statuses:
            # Usa get_or_create para obtener o crear el objeto
            OrderStatus.objects.get_or_create(status_name=status_name)
        
        self.stdout.write(self.style.SUCCESS("Successfully seeded the db"))