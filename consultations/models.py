from django_enumfield import EnumField

from django.db import models

from .enums import ConsultationStateEnum


class Consultation(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    closing_date = models.DateTimeField()

    state = EnumField(ConsultationStateEnum)

    def __str__(self):
        return "{self.title}: {self.closing_date}".format(self=self)
