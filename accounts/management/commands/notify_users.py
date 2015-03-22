from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from consultations.enums import ConsultationStateEnum
from consultations.models import Consultation


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.all():
            consultations = Consultation.objects.filter(
                state=ConsultationStateEnum.OPEN,
                topics__topic__users__user=user,
            )

            print(user, consultations)
