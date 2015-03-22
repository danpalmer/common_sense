from django.core.management.base import BaseCommand

from consultations.models import Consultation


class Command(BaseCommand):

    def handle(self, *args, **options):
        for consultation in Consultation.objects.all():
            pass
