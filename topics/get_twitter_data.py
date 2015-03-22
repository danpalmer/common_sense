#!/usr/bin/env python
# -*- encoding:utf-8 -*-

from __future__ import unicode_literals
from bs4 import BeautifulSoup
import datetime
import re
import requests
import tweepy


# Twitter handle of the user we're profiling
twitter_handle = 'graingert'


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

# Twitter creds
consumer_key = "TWITTER_OATH_KEY"
consumer_secret = "TWITTER_SECRET"
access_token = "TWITTER_ACCESS_TOKEN"
access_token_secret = "TWITTER_ACCESS_TOKEN_SECRET"

# Access Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
statuses = api.user_timeline(id=twitter_handle, count=100)

# Status text
out = []
for status in statuses:
    out.append(status.text)

# Status links
links = [re.findall(r'(https?://[^\s]+)', row) for row in out]
links = strip_links(links)
interesting_links = []
link_html = []
for link in links:
    try:
        response = requests.get(link)
        if response.status_code == 200:
            print(response.url)
            if (len(re.findall(r'(twitter.com/+)', response.url)) == 0 and
                len(re.findall(r'(swarmapp.com/+)', response.url)) == 0 and
                len(re.findall(r'(instagram.com/+)', response.url)) == 0 and
                len(re.findall(r'(i.imgur.com/+)', response.url)) == 0):
                interesting_links.append(response.url)
                link_html.append(response.text)
    except Exception:
        pass

raw_text = ' '.join(out).replace('\'', '').replace('#', '')
for this_page in link_html:
    soup = BeautifulSoup(this_page)
    texts = soup.findAll(text=True)
    visible_texts = list(filter(visible, texts))
    text = ' '.join(visible_texts).replace('\n', '').replace('\t', '')
    raw_text = raw_text + ' ' + text


with open(twitter_handle + '.txt', 'w') as f:
    f.write(raw_text)
