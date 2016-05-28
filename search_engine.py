import requests
from bs4 import BeautifulSoup


def download_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception('Non-OK status code: {}'.format(r.status_code))
    return r.text


def parse_text(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.select('div.usertext-body')[1].text

