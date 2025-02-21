from pathlib import Path
import json
import tokenizer


class Indexer:
    def __init__(self, hasher):
        self.hasher = hasher
        self.inverted_index = {}  # { token: { docId : (freq) }
        self.id_to_url = {}  # { docID: (url, hash) }
        self.doc_id = 0

    # HIGH PRIORITY
    def traverse(self, path_name):
        if Path("inverted_index.json") and Path("id_to_url"):
            self.start()

        root_dir = Path(path_name)
        try:
            for sub_dir in root_dir.glob("**"):  # Grabs subdirectories (effectively subdomains) for glob
                for json_file in sub_dir.glob("*.json"):  # Grabs actual json files attached to each subdomain
                    try:
                        url, content = self.file_parser(json_file)
                        self.push_to_inverted_index(url, content)

                    except json.JSONDecodeError:
                        print(f"Invalid JSON in {json_file}")
                    except PermissionError:
                        print(f"Permission denied for {json_file}")
                    except Exception as e:
                        print(f"Unexpected error with {json_file}: {e}")
            self.save_files("inverted_index.json", "id_to_url.json")
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    def file_parser(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data["url"]
            content = data["content"]
        return url, content

    # HIGH PRIORITY
    def push_to_inverted_index(self, url, content):
        current_id = self.assign_id(url, content)
        tokens = tokenizer.tokenize(content)

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

    def start(self):
        self.load_id_to_url("inverted_index.json")
        self.load_inverted_index("id_to_url.json")
        self.load_doc_id()

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
        return self.id_to_url[self.doc_id - 1][0]
