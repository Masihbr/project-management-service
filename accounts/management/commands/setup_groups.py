from django.core.management.base import BaseCommand
from accounts.authorizations import setup_groups

class Command(BaseCommand):
    help = 'creates groups and adds permissions'
    
    def add_arguments(self, parser):
        parser.add_argument('--logs', action='store_true', help='Print logs')
        
    def handle(self, *args, **options):
        logs_enabled = options.get('logs', False)
        setup_groups(quiet=not logs_enabled)