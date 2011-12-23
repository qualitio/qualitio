from django.core.management.base import BaseCommand
from ...models import Profile
from datetime import datetime

class Command(BaseCommand):
    help = "Manage payment profiles"

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            if profile.status == Profile.ACTIVE:
                if datetime.now() > profile.valid_time:
                    profile.cancel()
            
            if profile.status == Profile.PENDING:
                if (datetime.now() - profile.created_time).days > 1:
                    profile.cancel()
