import argparse
import json
import os
from util import *
import base64


class Indexer(object):
    def __init__(self):
        self.inverted_index = dict()
        self.forward_index = dict()
        self.url_to_id = dict()
        self.doc_count = 0

    def add_document(self, url, parsed_text):
        self.doc_count += 1
        assert url not in self.url_to_id
        current_id = self.doc_count
        self.url_to_id[url] = current_id
        self.forward_index[current_id] = parsed_text
        for position, word in enumerate(parsed_text):
            if word != '':
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                self.inverted_index[word].append((position, current_id))

    def store_on_disk(self, index_dir):

        def dump_json_to_file(source, file_name):
            file_path = os.path.join(index_dir, file_name)
            json.dump(source, open(file_path, 'w'), indent=4)

        dump_json_to_file(self.inverted_index, 'inverted_index')
        dump_json_to_file(self.forward_index, 'forward_index')
        dump_json_to_file(self.url_to_id, 'url_to_id')

class Searcher(object):
    def __init__(self, index_dir):
        self.inverted_index = dict()
        self.forward_index = dict()
        self.url_to_id = dict()

        def load_json_from_file(file_name):
            file_path = os.path.join(index_dir, file_name)
            return json.load(open(file_path))

        self.inverted_index = load_json_from_file('inverted_index')
        self.forward_index = load_json_from_file('forward_index')
        self.url_to_id = load_json_from_file('url_to_id')

    def find_documents(self, words):
        return sum([self.inverted_index[word] for word in words], [])

def create_index_from_dir(stored_documents_dir, index_dir):
    indexer = Indexer()
    for filename in os.listdir(stored_documents_dir):
        print stored_documents_dir, filename

        opened_file = open(os.path.join(stored_documents_dir, filename))
        parsed_doc = parse_reddit_post(opened_file.read()).split(' ')
        indexer.add_document(base64.b16encode(filename), parsed_doc)
        opened_file.close()
    indexer.store_on_disk(index_dir)


def main():
    parser = argparse.ArgumentParser(description='Index /r/learnprogramming')
    parser.add_argument('--stored_documents_dir', dest='stored_documents_dir', required=True)
    parser.add_argument('--index_dir', dest='index_dir', required=True)
    args = parser.parse_args()
    create_index_from_dir(args.stored_documents_dir, args.index_dir)

if __name__ == "__main__":
    main()
