from django.db import models


class Vote(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{self.title}: {self.date}".format(self=self)
