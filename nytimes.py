#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import json
import codecs


class NYTimes(object):
    host = 'https://www.nytimes.com'

    def __init__(self):
        self.session = requests.Session()
        self.session.headers['user-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.art_links = json.load(open('news.json'))
        text = codecs.open('text.txt', 'w', encoding='utf-8')
        for a in self.art_links:
            a['text'] = self.article(a['html'])
            if not a['text'] or not self.is_english(a['text']):
                if a and 'link' in a:
                    print(a['link'])
                    print(a['text'])
                continue
            text.write(a['title'])
            text.write('\n')
            text.write(a['text'])
            text.write('\n')
            text.write('\n')
        text.close()
        with open('text2.json', 'w+b') as f:
            f.write(json.dumps(self.art_links))

    def is_english(self, text):
        ret = 1.0 * len(re.findall('[a-zA-Z]', text)) / len(text)
        return ret > 0.1

    def get(self, url, **kwargs):
        self.session.cookies.clear()
        return self.session.get(url, **kwargs)

    def article(self, html):
        soup = BeautifulSoup(html, 'lxml')
        return '\n'.join([p.text for p in soup.find_all('p', 'story-content')])

    def protal(self):
        def get_article(anode):
            head = anode.findChild(re.compile('h[1|2]'), 'story-heading')
            a = head.findChild('a') if head else None
            if a and a['href'].endswith('.html'):
                return (a['href'], a.text.replace('\n', '').strip())
            else:
                return None

        def get_date(url):
            date = re.findall('(\d+)/(\d+)/(\d+)', url)
            return ''.join(date[0]) if date else '0'

        def is_english(text):
            return len(re.findall('[a-zA-Z]', text)) / len(text) > 0.8

        nyt = self.get(self.host)
        soup = BeautifulSoup(nyt.text, 'lxml')
        art_links = list(
                set(filter(bool, map(get_article, soup.find_all('article')))))
        art_links.sort(key=lambda a: int(get_date(a[0])), reverse=True)
        art_links = [{'link': a[0], 'title': a[1]} for a in art_links]
        for a in art_links:
            a['html'] = self.get(a['link']).content
            a['text'] = self.article(a['html'])
        art_links = filter(lambda a: is_english(a['text']), art_links)
        with open('news.json', 'w+b') as f:
            f.write(json.dumps(art_links))
        print(len(art_links))
nyt = NYTimes()
# nyt.protal()
