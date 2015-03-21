from bs4 import BeautifulSoup
import requests
import re

# Get JSON of all open consultations
url = 'https://www.gov.uk/government/publications.json?keywords=&publication_filter_option=open-consultations&topics%5B%5D=all&departments%5B%5D=all&official_document_status=all&world_locations%5B%5D=all&from_date=&to_date='
response = requests.get(url)
if response.status_code == 200:
    response_json = response.json()

# Extract some features
consultations = []
for consultation in response_json['results']:
    consultation_id = consultation['id']
    organisation = consultation['organisations']
    time = consultation['public_timestamp']
    title = consultation['title']
    url = consultation['url']

    # Let's go look at the consultation page
    consultation_details_response = requests.get('https://www.gov.uk/' + url)
    if (consultation_details_response.status_code == 200):
        consultation_details = consultation_details_response.text

    soup = BeautifulSoup(consultation_details)

    first_published = soup.find('aside', class_='metadata-list').find('abbr', class_='date').attrs['title']
    consultation_closes = soup.find('div', class_='consultation-dates').find('abbr', class_='closing-at').attrs['title']
    summary = soup.find('div', class_='consultation-summary-inner').find('p').text
    description = soup.findAll('h1', text = re.compile('Consultation description'))[0].parent.next_sibling.next_sibling.find('div', class_='govspeak').find('p').text
    contact_email = soup.find('dd', class_ = 'email').find('a').text
    contact_address = str(soup.find('dd', class_ = 'postal-address'))
    contact_address = contact_address.replace('<dd class="postal-address">', '').replace('<br>', ', ').replace('</br>', '').replace('</dd>', '')

    consultation_data = {
        'consultation_id': consultation_id,
        'organisation': organisation,
        'time': time,
        'title': title,
        'url': url,
        'first_published': first_published,
        'consultation_closes': consultation_closes,
        'summary': summary,
        'description': description,
        'contact_email': contact_email,
        'contact_address': contact_address,
        'documents': []
    }

    print(consultation_data)

    # Let's go look at the related documents
    documents = soup.find('h1', text = re.compile(r'Documents')).parent.parent.findAll('section', class_ = 'attachment')
    for document in documents:
        document_id = document.attrs['id']
        document_type = document.find('p', class_ = 'metadata').find('span', class_ = 'type').find('abbr').text
        document_url = 'https://www.gov.uk' + document.find('h2', class_ = 'title').find('a').attrs['href']
        document_response = requests.get(document_url)
        if (response.status_code == 200):
            response_json = response.json()
        consultation_data['documents'].append({
            'document_id': document_id,
            'document_type': document_type,
            'document_url': document_url
            })

    # Save it to a dict so we can do what we want
    consultations.append(consultation_data)
    print(consultation_data)
