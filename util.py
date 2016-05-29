import requests
from bs4 import BeautifulSoup
import os.path
from base64 import b16encode
import time
import argparse


def download_reddit_url(url):
    assert url.startswith('https://www.reddit.com/r/learnprogramming')
    headers = {'User-Agent':'JustSearch bot version 0.1'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception('Non-OK status code: {}'.format(r.status_code))
    return r.text


def parse_reddit_post(html):
    bs = BeautifulSoup(html)
    #print bs.select('div.usertext-body')[1].text
    return bs.select('div.usertext-body')[1].text
