from django.core.management.base import BaseCommand, CommandError
from votes.models import Vote


class Command(BaseCommand):

    def handle(self, *args, **options):
        raise NotImplementedError()
