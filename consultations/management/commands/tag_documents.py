import io
import csv
import subprocess

from django.core.management.base import BaseCommand

from consultations.models import Consultation, Topic


class Command(BaseCommand):

    def handle(self, *args, **options):
        with io.String() as stdout:
            subprocess.call("Rscript topics/tag_consultations.R", stdout=stdout)
            csv_reader = csv.reader(stdout)
            for consultation_id, tags in csv_reader:
                consultation = Consultation.objects.get(pk=consultation_id)

                consultation_topic_ids = []
                for tag in [x.strip() for x in tags.split(',')]:
                    topic = Topic.objects.get_or_create(name=tag)
                    consultation.topics.get_or_create(topic=topic)

                    consultation_topic_ids.append(topic.pk)

                    Consultation.topics.exclude(
                        topic__id__in=consultation_topic_ids,
                    ).delete()
