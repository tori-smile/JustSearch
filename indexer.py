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
        self.forward_index[current_id] = parsed_text
        for position, word in enumerate(parsed_text):
            if word != '':
                if word not in self.inverted_index:
                    self.inverted_index[word] = []
                self.inverted_index[word].append((position, current_id))

    def store_on_disk(self, index_dir):
        inverted_index_file_name = os.path.join(index_dir, 'inverted_index')
        forward_index_file_name = os.path.join(index_dir, 'forward_index')
        url_to_id_file_name = os.path.join(index_dir, 'url_to_id')

        inverted_index_file = open(inverted_index_file_name, 'w')
        forward_index_file = open(forward_index_file_name, 'w')
        url_to_id_file = open(url_to_id_file_name, 'w')

        json.dump(self.inverted_index, inverted_index_file, indent=4)
        json.dump(self.forward_index, forward_index_file, indent=4)
        json.dump(self.url_to_id, url_to_id_file, indent=4)


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
    parser.add_argument('--stored_documents_dir', dest='stored_documents_dir')
    parser.add_argument('--index_dir', dest='index_dir')
    args = parser.parse_args()
    create_index_from_dir(args.stored_documents_dir, args.index_dir)

if __name__ == "__main__":
    main()
