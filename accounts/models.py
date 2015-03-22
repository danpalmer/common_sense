from django.db import models
from django.contrib.auth.models import User

from consultations.models import Topic


class UserTopic(models.Model):
    user = models.ForeignKey(User, related_name='topics')
    topic = models.ForeignKey(Topic, related_name='users')


class UserTwitterData(models.Model):
    user = models.OneToOneField(User, related_name='twitter_data')
    data = models.TextField(blank=True)
