import bs4
import arrow
import requests

from urllib.parse import urljoin

from django.core.management.base import BaseCommand, CommandError

from consultations.models import Consultation
from consultations.enums import ConsultationStateEnum


class Command(BaseCommand):

    def handle(self, *args, **options):
        session = requests.Session()

        response = session.get(
            'https://www.gov.uk/government/publications.json?'
            'publication_filter_option=consultations'
        )

        response.raise_for_status()
        data = response.json()

        for publication in data['results']:
            if publication['type'] != 'consultation':
                continue

            consultation_state = \
                ConsultationStateEnum.DISPLAY_TYPE_TO_ENUM_TYPE.get(
                    publication['display_type']
                )

            if not consultation_state:
                continue

            publication_url = urljoin(response.url, publication['url'])
            publication_doc = session.get(publication_url)

            root = bs4.BeautifulSoup(publication_doc.content)

            closing_date_str = root.select('.closing-at')[0]['title']
            closing_date = arrow.get(closing_date_str).to('utc').datetime

            consultation, created = Consultation.objects.get_or_create(
                url=publication_url,
                defaults={
                    'title': publication['title'],
                    'state': consultation_state,
                    'closing_date': closing_date,
                }
            )

            if created:
                print(consultation.title)
