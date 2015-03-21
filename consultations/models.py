from django_enumfield import EnumField

from django.db import models

from .enums import ConsultationStateEnum


class Consultation(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    closing_date = models.DateTimeField()

    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)

    state = EnumField(ConsultationStateEnum)

    def __str__(self):
        return "{self.title}: {self.closing_date}".format(self=self)
