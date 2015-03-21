from django.core.management.base import BaseCommand, CommandError
from consultations.models import Consultation


class Command(BaseCommand):

    def handle(self, *args, **options):
        raise NotImplementedError()
