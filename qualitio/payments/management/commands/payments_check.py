from django.core.management.base import BaseCommand
from ...models import Profile
from datetime import datetime

class Command(BaseCommand):
    help = "Manage payment profiles"

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            if datetime.now().date() > profile.valid_till:
                print profile.status