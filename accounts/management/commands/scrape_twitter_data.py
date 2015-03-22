from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.filter(twitter_data__isnull=True):
            print user
