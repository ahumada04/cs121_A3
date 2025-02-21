class Indexer:
    def __init__(self, hasher):
        self.hasher = hasher
        inverted_index = {}  # { token: { docId : (freq) }
        id_to_url = {}  # { docID: (url, hash) }
        doc_id = 0

    # HIGH PRIORITY
    def traverse(self, path):
        pass

    # HIGH PRIORITY
    def push_to_inverted_index(self, tokens, url):
        pass

    # HIGH PRIORITY
    def assign_id(self, url, content):
        pass

    # low priority
    def load_inverted_index(self, file_path):
        pass

    # low priority
    def load_id_to_url(self, file_path):
        pass

    # low priority
    def load_doc_id(self):
        pass

    # low priority
    def save_files(self):
        pass

    # low priority
    def grab_last_indexed(self):
        pass


def tokenize(content) -> list:
    pass







