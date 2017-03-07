#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import os
import re
import time


class TTS(object):
    host = 'http://www.fromtexttospeech.com'

    def __init__(self, text, mp3file):
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        self.session.headers['Host'] = 'www.fromtexttospeech.com'
        self.session.headers['Referer'] = 'http://www.fromtexttospeech.com/'
        form_data = {
            'input_text': text,
            'language': 'US English',
            'voice': 'IVONA Kimberly22',
            'speed': 0,
            'action': 'process_text'
        }
        html = self.post(self.host, data=form_data).content
        mp3url = re.findall('<a href=\'([^>]+)\'>Download audio file', html)
        if not mp3url:
            print("errr")
            return

        mp3data = self.get(self.host + mp3url[0])
        with open(mp3file, 'w+b') as f:
            f.write(mp3data.content)
        with open(os.path.splitext(mp3file)[0] + '.txt', 'w+b') as f:
            f.write(text)

    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

cnt = 1
for f in os.sys.argv[1:]:
    chapters = re.split(r'(?m)^\s*$\s*', open(f).read())
    i = 0
    total_len = 0
    pos = [0]
    for i in range(0, len(chapters)):
        if total_len + len(chapters[i]) >= 50000:
            pos.append(i)
            total_len = len(chapters[i])
        else:
            total_len += len(chapters[i])
    pos.append(len(chapters))
    print(pos)
    for v in pos[1:]:
        prv = pos[pos.index(v) - 1]
        text = '\n\n'.join(chapters[prv:v])
        print('text len:%d' % len(text))
        TTS(text=text, mp3file='out3/nytnews_chapter{d}.mp3'.format(d=cnt))
        cnt += 1
        time.sleep(60)
