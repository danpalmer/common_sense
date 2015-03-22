from bs4 import BeautifulSoup
import codecs
import csv
import os
import requests
import re
import subprocess
from urllib.request import urlopen


# Get JSON of all open consultations
url = 'https://www.gov.uk/government/publications.json?keywords=&publication_filter_option=open-consultations&topics%5B%5D=all&departments%5B%5D=all&official_document_status=all&world_locations%5B%5D=all&from_date=&to_date='
response = requests.get(url)
if response.status_code == 200:
    response_json = response.json()

# Extract some features
consultations = [[
    'consultation_id',
    'organisation',
    'time',
    'title',
    'url',
    'summary',
    'description',
    'raw_text'
]]

# Useful for hiding output of subprocess.call()
FNULL = open(os.devnull, 'w')

# Iterate over consultations
for consultation in response_json['results']:
    consultation_id = consultation['id']
    organisation = consultation['organisations']
    time = consultation['public_timestamp']
    title = consultation['title']
    url = consultation['url']

    print('\n' + title)

    # Let's go look at the consultation page
    consultation_details_response = requests.get('https://www.gov.uk/' + url)
    if (consultation_details_response.status_code == 200):
        consultation_details = consultation_details_response.text
    soup = BeautifulSoup(consultation_details)
    summary = soup.find('div', class_='consultation-summary-inner').find('p').text
    description = soup.find('h1', text = re.compile('Consultation description')).parent.next_sibling.next_sibling.find('div', class_='govspeak').find('p').text
    
    consultation_data = [
        str(consultation_id),
        organisation,
        time,
        title,
        url,
        summary,
        description
    ]

    document_raw_text = ""

    # Let's go look at the related documents
    if soup.find('h1', text = re.compile(r'Documents')):
        documents = soup.find('h1', text = re.compile(r'Documents')).parent.parent.findAll('section', class_ = 'attachment')
        for document in documents:
            document_id = document.attrs['id']
            document_type = document.find('p', class_ = 'metadata').find('span', class_ = 'type').text
            document_url = 'https://www.gov.uk' + document.find('h2', class_ = 'title').find('a').attrs['href']
            document_name = document.find('h2', class_ = 'title').find('a').text
            print('\t' + document_name)

            if document_type == 'PDF':
                document_response = urlopen(document_url)
                pdf_filename = 'pdfs/' + document_name + '.pdf'
                txt_filename = 'txts/' + document_name + '.txt'
                with open(pdf_filename, 'wb') as pdf:
                    pdf.write(document_response.read())
                    pdf.close()
                command = "pdf2txt.py -t text -o '" + txt_filename + "' '" + pdf_filename + "'"
                subprocess.call([command], shell=True, stdout=FNULL, stderr=subprocess.STDOUT)
                with codecs.open(txt_filename,'r', encoding='utf8') as f:
                    text = f.read()
            else:
                text = ""
            document_raw_text = document_raw_text + " " + text
    else:
        document_raw_text = ""

    consultation_data.append(document_raw_text)
    consultations.append(consultation_data)
        
# Finally save the lot into a CSV for ease of processing
with open('consultations.csv', 'w', newline='') as csvfile:
    w = csv.writer(csvfile)
    for entry in consultations:
        w.writerow(entry)
