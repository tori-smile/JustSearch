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
    bs = BeautifulSoup(html, 'html.parser')
    return bs.select('div.usertext-body')[1].text


class Crawler(object):
    def __init__(self, start_url, storage_dir):
        self.start_url = start_url
        self.storage_dir = storage_dir

    @staticmethod
    def _make_absolute_url(url):
        return 'https://www.reddit.com' + url

    def crawl(self):
        current_page_url = self.start_url
        while True:
            current_page = download_reddit_url(current_page_url)
            bs = BeautifulSoup(current_page)
            all_posts_links = bs.findAll('a', attrs={'class': 'title'})
            post_links = [Crawler._make_absolute_url(link['href']) for link in all_posts_links]
            for post_link in post_links:
                html = download_reddit_url(post_link)
                stored_text_file_name = os.path.join(self.storage_dir, b16encode(post_link))
                stored_text_file = open(stored_text_file_name, 'w')
                stored_text_file.write(html.encode('utf8'))
                stored_text_file.close()
            next_page_url = bs.find('a', attrs={'rel':'next'})['href']
            current_page_url = next_page_url
            time.sleep(2)
            print  next_page_url


def main():
    parser = argparse.ArgumentParser(description='Crawl /r/learnprogramming')
    parser.add_argument('--start_url', dest='start_url')
    parser.add_argument('--storage_dir', dest='storage_dir')
    args = parser.parse_args()
    print args.start_url, args.storage_dir
    crawler = Crawler(args.start_url, args.storage_dir)
    crawler.crawl()

if __name__ == "__main__":
    main()