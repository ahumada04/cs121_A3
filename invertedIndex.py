import pathlib
import json


class Indexer:
    def __init__(self, hasher):
        self.hasher = hasher
        self.inverted_index = {}  # { token: { docId : (freq) }
        self.id_to_url = {}  # { docID: (url, hash) }
        self.doc_id = 0

    # HIGH PRIORITY
    def traverse(self, path):
        pass

    def file_parser(self):
        pass

    # HIGH PRIORITY
    def push_to_inverted_index(self, url, content):
        current_id = self.assign_id(url, content)
        tokens = tokenize(content)

        for token in tokens.keys():
            frequency = tokens[token]
            if token not in self.inverted_index:
                self.inverted_index[token] = {current_id: frequency}
            else:
                self.inverted_index[token].update({current_id: frequency})

    # HIGH PRIORITY
    def assign_id(self, url, content):
        if self.doc_id in self.id_to_url:
            self.id_to_url[self.doc_id] = (url, self.hasher.hash(content))
            return self.doc_id
        else:
            self.doc_id = max(self.id_to_url.keys()) + 1
            self.assign_id(content, url)

    # low priority
    def load_inverted_index(self, file_path):
        with open(file_path, "r") as file:
            self.inverted_index = json.load(file)

    # low priority
    def load_id_to_url(self, file_path):
        with open(file_path, "r") as file:
            self.id_to_url = json.load(file)

    # low priority
    def load_doc_id(self):
        self.doc_id = max(self.id_to_url.keys()) + 1

    # low priority
    def save_files(self, inverted_index_path, id_to_url_path):
        with open(inverted_index_path, "w", encoding="utf-8") as inverted_index_file:
            json.dump(self.inverted_index, inverted_index_file, indent=4, ensure_ascii=False)

        with open(id_to_url_path, "w", encoding="utf-8") as id_to_url_file:
            json.dump(self.id_to_url, id_to_url_file, indent=4, ensure_ascii=False)

    # low priority
    def grab_last_indexed(self):
        pass


def tokenize(content) -> dict:
    pass







