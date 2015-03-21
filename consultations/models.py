from django.db import models


class Consultation(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    organisation = models.CharField(max_length=200)
    closing_date = models.DateTimeField()
