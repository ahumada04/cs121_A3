from pathlib import Path
import json
import tokenizer
import os
from bs4 import BeautifulSoup
import hasher


def main():
    simhash = hasher.SimHash()
    indexer = Indexer(simhash)
    indexer.traverse("TESTDEV")


class Indexer:
    def __init__(self, hasher):
        self.hasher = hasher
        self.inverted_index_0_9 = {}  # { token: { docId : (freq, bold, position) }
        self.inverted_index_a_h = {}  # { token: { docId : (freq, bold, position) }
        self.inverted_index_i_q = {}  # { token: { docId : (freq, bold, position) }
        self.inverted_index_r_z = {}  # { token: { docId : (freq, bold, position) }
        self.id_to_url = {}  # { docID: (url, hash) }
        self.doc_id = 0

    # HIGH PRIORITY
    def traverse(self, path_name):
        if os.path.exists("inverted_index_0_9.json"):
            os.remove("inverted_index_0_9.json")

        if os.path.exists("inverted_index_a_h.json"):
            os.remove("inverted_index_a_h.json")

        if os.path.exists("inverted_index_i_q.json"):
            os.remove("inverted_index_i_q.json")

        if os.path.exists("inverted_index_r_z.json"):
            os.remove("inverted_index_r_z.json")

        if os.path.exists("id_to_url.json"):
            os.remove("id_to_url.json")

        root_dir = Path(path_name)
        try:
            count = 0
            for sub_dir in root_dir.glob("**"):  # Grabs subdirectories (effectively subdomains) for glob
                count += 1
                print(count)
                for json_file in sub_dir.glob("*.json"):  # Grabs actual json files attached to each subdomain
                    try:
                        url, content, title, heading, bold_text = self.file_parser(json_file)
                        self.push_to_inverted_index(url, content, title, heading, bold_text)

                    except json.JSONDecodeError:
                        print(f"Invalid JSON in {json_file}")
                    except PermissionError:
                        print(f"Permission denied for {json_file}")
                    except Exception as e:
                        print(f"Unexpected error with {json_file}: {e}")

            self.save_files("id_to_url.json")
            self.merge_files()
        except Exception as e:
            print(f"Unexpected error: {e}")

    @staticmethod
    # ERICK: json dump between 
    def file_parser(json_file):
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)
            url = data["url"]
            # content = data["content"]
            soup = BeautifulSoup(data["content"], "lxml")
            # Extract different text parts (text, titles, headings, bold)
            content = soup.get_text()                                                          # ARBITRARY SCORES FOR NOW
            title = " ".join([tag.get_text() for tag in soup.find_all("title")])               # x2 score multiplier
            heading = " ".join([tag.get_text() for tag in soup.find_all(["h1", "h2", "h3"])])  # x1.5 score multiplier
            bold_text = " ".join([tag.get_text() for tag in soup.find_all(["b", "strong"])])   # x1.2 score multiplier

        return url, content, title, heading, bold_text

    # HIGH PRIORITY
    # MODIFIED
    # Updating with pran code
    def push_to_inverted_index(self, url, content, title, heading, bold_text):
        # raw token/ term frequency
        tokens = tokenizer.tokenize(content)
        tokens_dict = tokenizer.computeWordFrequencies(tokens)

        title_set = set(tokenizer.tokenize(title))
        heading_set = tokenizer.computeWordFrequencies(heading)
        bold_set = tokenizer.tokenize(bold_text)

        current_id = self.assign_id(url, tokens)

        for token, frequency in tokens_dict.items():
            # Fluffing up frequency count within a document to increase TF-IDF score
            # Update scores AS WE GO
            if token in title_set:
                frequency = frequency * 2
            if token in heading_set:
                frequency = frequency * 1.5
            if token in bold_set:
                frequency = frequency * 1.2

            starting_char = token[0]

            if "0" <= starting_char <= "9":
                if token not in self.inverted_index_0_9:
                    self.inverted_index_0_9[token] = {current_id: frequency}
                else:
                    self.inverted_index_0_9[token].update({current_id: frequency})

            elif "a" <= starting_char <= "h":
                if token not in self.inverted_index_a_h:
                    self.inverted_index_a_h[token] = {current_id: frequency}
                else:
                    self.inverted_index_a_h[token].update({current_id: frequency})

            elif "i" <= starting_char <= "q":
                if token not in self.inverted_index_i_q:
                    self.inverted_index_i_q[token] = {current_id: frequency}
                else:
                    self.inverted_index_i_q[token].update({current_id: frequency})
            else:
                if token not in self.inverted_index_r_z:
                    self.inverted_index_r_z[token] = {current_id: frequency}
                else:
                    self.inverted_index_r_z[token].update({current_id: frequency})

            # self.inverted_index[token].update({current_id: frequency})

    # HIGH PRIORITY
    def assign_id(self, url: str, tokens: list):
        if self.doc_id not in self.id_to_url:
            self.id_to_url[self.doc_id] = (url, self.hasher.compute(tokens))
            self.doc_id += 1
            return self.doc_id - 1
        else:
            self.doc_id = max(self.id_to_url.keys()) + 1
            self.assign_id(url, tokens)

    # low priority
    def save_files(self, id_to_url_path):
        with open("inverted_index_path_0_9.json", "w", encoding="utf-8") as inverted_index_file:
            json.dump(self.inverted_index_0_9, inverted_index_file, indent=4, ensure_ascii=False)

        with open("inverted_index_path_a_h.json", "w", encoding="utf-8") as inverted_index_file:
            json.dump(self.inverted_index_a_h, inverted_index_file, indent=4, ensure_ascii=False)

        with open("inverted_index_path_i_q.json", "w", encoding="utf-8") as inverted_index_file:
            json.dump(self.inverted_index_i_q, inverted_index_file, indent=4, ensure_ascii=False)

        with open("inverted_index_path_r_z.json", "w", encoding="utf-8") as inverted_index_file:
            json.dump(self.inverted_index_r_z, inverted_index_file, indent=4, ensure_ascii=False)

        with open(id_to_url_path, "w", encoding="utf-8") as id_to_url_file:
            json.dump(self.id_to_url, id_to_url_file, indent=4, ensure_ascii=False)

    @staticmethod
    def merge_files():
        json_files = ["inverted_index_path_0_9.json", "inverted_index_path_a_h.json",
                      "inverted_index_path_i_q.json", "inverted_index_path_r_z.json"]
        merged_data = {}

        for file in json_files:
            if os.path.exists(file):
                try:
                    with open(file, "r") as f:
                        data = json.load(f)
                        for key, value in data.items():
                            if key in merged_data:
                                print(f"Warning: Key '{key}' from {file} already exists. Keeping original value.")
                            else:
                                merged_data[key] = value
                except json.JSONDecodeError:
                    print(f"Skipping {file} due to JSON format error.")

        with open("merged.json", "w") as f:
            json.dump(merged_data, f, indent=4)


if __name__ == "__main__":
    main()


# OG NGUYEN CODE, KEEP FOR NOW JUST INCASE WE RUN INTO WEIRD ERRORS
# def query_document_match(self, query) -> list:
#     query_tokens = tokenizer.tokenize(query)
#     intersection_queue = []
#
#     for token in query_tokens:
#         if token in self.inverted_index:
#             intersection_queue.append(list(self.inverted_index[token].keys()))
#         else:
#             return []
#
#     intersection_queue = sorted(intersection_queue, key=lambda item: len(item))
#     intersection = intersection_queue[0]
#     for i in range(1, len(intersection_queue)):
#         intersection = self.intersect(intersection, intersection_queue[i])
#
#     return intersection
#
# @staticmethod
# def intersect(term_list1, term_list2):
#     answer = []
#     i = 0
#     j = 0
#     while i < len(term_list1) and j < len(term_list2):
#         if term_list1[i] == term_list2[j]:
#             answer.append(term_list1[i])
#             i += 1
#             j += 1
#         elif term_list1[i] > term_list2[j]:
#             j += 1
#         else:
#             i += 1
#     return answer
#
