import io
import csv
import subprocess

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from consultations.models import Topic


class Command(BaseCommand):

    def handle(self, *args, **options):
        with io.String() as stdout:
            subprocess.call("Rscript tag_twitter_data.R", stdout=stdout)
            csv_reader = csv.reader(stdout)
            for user_id, tags in csv_reader:
                user = User.objects.get(pk=user_id)

                for tag in [x.strip() for x in tags.split(',')]:
                    topic = Topic.objects.get_or_create(name=tag)
                    user.topics.get_or_create(topic=topic)
