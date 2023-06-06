from django.core.management.base import BaseCommand
from accounts.authorizations import setup_groups

class Command(BaseCommand):
    help = 'creates groups and adds permissions'
    
    def handle(self, *args, **options):
        setup_groups()