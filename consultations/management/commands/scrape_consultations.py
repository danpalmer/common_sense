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
        print("    URL:", publication_url)

        publication_doc = self.session.get(publication_url)

        root = bs4.BeautifulSoup(publication_doc.content)

        closing_date_str = root.select('.closing-at')[0]['title']
        closing_date = arrow.get(closing_date_str).to('utc').datetime

        try:
            summary = root.find(
                'div', class_='consultation-summary-inner'
            ).find('p').text
        except:
            summary = ''

        contact_email = ''
        contact_address = ''
        response_form = ''
        response_document = ''

        response_formats = root.find('section', id='response-formats')
        if response_formats:
            try:
                contact_email = response_formats.find('dd', class_ = 'email').find('a').text
            except:
                pass
            try:
                contact_address = '\n'.join(response_formats.find('dd', class_ = 'postal-address').stripped_strings)
            except:
                pass
            try:
                response_form = response_formats.find(class_='response-form').find('a').attrs['href']
            except:
                pass
            try:
                response_document = response_formats.find(class_='online').find('a').attrs['href']
            except:
                pass

        return {
            'url': publication_url,
            'title': publication['title'],
            'state': consultation_state,
            'closing_date': closing_date,
            'contact_email': contact_email,
            'contact_address': contact_address,
            'summary': summary,
            'response_form': response_form,
            'response_document': response_document,
        }
