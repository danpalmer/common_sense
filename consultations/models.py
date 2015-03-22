from datetime import datetime
import bleach

from django_enumfield import EnumField

from django.db import models
from django.utils.safestring import mark_safe

from .enums import ConsultationStateEnum


class Consultation(models.Model):
    url = models.URLField(unique=True, max_length=2048)
    title = models.CharField(max_length=500)
    closing_date = models.DateTimeField()
    last_update = models.DateTimeField(default=datetime.now)
    organisation = models.TextField(blank=True)
    organisation_abbr = models.TextField(blank=True)

    summary = models.TextField(blank=True)

    contact_email = models.EmailField(blank=True)
    contact_address = models.TextField(blank=True)
    response_form = models.URLField(blank=True)
    response_document = models.URLField(blank=True)

    raw_text = models.TextField(blank=True)

    state = EnumField(ConsultationStateEnum)

    def __str__(self):
        return "{self.title}: {self.closing_date}".format(self=self)

    def cleaned_description(self):
        print(self.description)
        return mark_safe(
            bleach.clean(
                self.description,
                tags=('section', 'p', 'a', ),
                strip=True,
            ),
        )


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class ConsultationTopic(models.Model):
    topic = models.ForeignKey(Topic, related_name='consultations')
    consultation = models.ForeignKey(Consultation, related_name='topics')

    def __str__(self):
        return "{self.consultation.name}: {self.topic.name}".format(self=self)
