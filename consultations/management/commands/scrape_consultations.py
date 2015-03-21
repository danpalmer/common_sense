import re
import bs4
import arrow
import requests

from urllib.parse import urljoin

from django.core.management.base import BaseCommand

from consultations.models import Consultation
from consultations.enums import ConsultationStateEnum


class Command(BaseCommand):

    session = requests.Session()

    def handle(self, *args, **options):
        total_pages = 1
        current_page = 1

        while current_page <= total_pages:
            print("Scraping page: %d" % current_page)

            response = self.session.get(
                'https://www.gov.uk/government/publications.json',
                params={
                    'publication_filter_option': 'consultations',
                    'page': current_page,
                }
            )

            response.raise_for_status()
            data = response.json()

            for publication in data['results']:
                consultation_data = self.parse_publication(
                    publication,
                    response.url,
                )

                if not consultation_data:
                    continue

                consultation, created = Consultation.objects.get_or_create(
                    url=consultation_data['url'],
                    defaults=consultation_data,
                )

            current_page += 1
            total_pages = data['total_pages']

    def parse_publication(self, publication, base_url):
        if publication['type'] != 'consultation':
            return None

        consultation_state = \
            ConsultationStateEnum.DISPLAY_TYPE_TO_ENUM_TYPE.get(
                publication['display_type']
            )

        if not consultation_state:
            return None

        print("  Scraping consultation:", publication['title'])

        publication_url = urljoin(base_url, publication['url'])
        publication_doc = self.session.get(publication_url)

        root = bs4.BeautifulSoup(publication_doc.content)

        closing_date_str = root.select('.closing-at')[0]['title']
        closing_date = arrow.get(closing_date_str).to('utc').datetime

        summary = root.find(
            'div', class_='consultation-summary-inner'
        ).find('p').text

        description = root.findAll(
            'h1', text=re.compile('Consultation description')
        )[0].parent.next_sibling.next_sibling.find(
            'div', class_='govspeak'
        ).find('p').text

        contact_email = root.find('dd', class_='email').find('a').text

        contact_address = str(root.find('dd', class_='postal-address'))
        contact_address = contact_address.replace(
            '<dd class="postal-address">', ''
        ).replace('<br>', ', ').replace('</br>', '').replace('</dd>', '')

        return {
            'url': publication_url,
            'title': publication['title'],
            'state': consultation_state,
            'closing_date': closing_date,
            'contact_email': contact_email,
            'summary': summary,
            'description': description,
        }
