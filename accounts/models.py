from django.db import models
from django.contrib.auth.models import User

from consultations.models import Topic


class UserTopic(models.Model):
    user = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, related_name='users', on_delete=models.CASCADE)


class UserTwitterData(models.Model):
    user = models.OneToOneField(User, related_name='twitter_data', on_delete=models.CASCADE)
    data = models.TextField(blank=True)
