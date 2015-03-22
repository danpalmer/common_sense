import re
import tweepy
import requests

from bs4 import BeautifulSoup

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from allauth.socialaccount.models import SocialApp

from accounts.models import UserTwitterData


class Command(BaseCommand):

    session = requests.Session()

    def handle(self, *args, **options):
        for user in User.objects.filter(
            twitter_data__isnull=True,
            socialaccount__isnull=False,
        ):
            self.scrape(user)

    def scrape(self, user):
        twitter_account = user.socialaccount_set.all()[0]
        twitter_handle = twitter_account.extra_data['screen_name']
        twitter_token = twitter_account.socialtoken_set.all()[0]

        twitter = SocialApp.objects.all().first()

        auth = tweepy.OAuthHandler(twitter.client_id, twitter.secret)

        auth.set_access_token(twitter_token.token, twitter_token.token_secret)
        api = tweepy.API(auth)
        statuses = api.user_timeline(id=twitter_handle, count=300)

        # Status text
        out = []
        for status in statuses:
            out.append(status.text)

        # Status links
        links = [re.findall(r'(https?://[^\s]+)', row) for row in out]
        links = strip_links(links)

        urls = []
        for status in statuses:
            for url in status.entities['urls']:
                urls.append(url['expanded_url'])

        url_contents = []
        for url in urls:
            try:
                if (
                    len(re.findall(r'(twitter.com/+)', url)) == 0 and
                    len(re.findall(r'(swarmapp.com/+)', url)) == 0 and
                    len(re.findall(r'(instagram.com/+)', url)) == 0 and
                    len(re.findall(r'(i.imgur.com/+)', url)) == 0 and
                    len(re.findall(r'\.(jpg|png|ogg)$', url)) == 0
                ):
                    response = self.session.get(url)
                    if response.status_code == 200:
                        print(response.url)
                        url_contents.append(response.text)
            except Exception:
                pass

        raw_text = ' '.join(out).replace('\'', '').replace('#', '')
        for this_page in url_contents:
            soup = BeautifulSoup(this_page)
            texts = soup.findAll(text=True)
            visible_texts = list(filter(visible, texts))
            text = ' '.join(visible_texts).replace('\n', '').replace('\t', '')
            raw_text = raw_text + ' ' + text

        raw_text = re.sub(r'@\w+', '', raw_text)

        UserTwitterData.objects.create(
            user=user,
            data=raw_text,
        )


# Turns [[1, 2], [3]] into [1, 2, 3]
def strip_links(list_of_links):
    out = []
    for item in list_of_links:
        if len(item) > 0:
            for x in item:
                out.append(x.replace(')', ''))
    return(out)


# Is an element visible on a web page?
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True
