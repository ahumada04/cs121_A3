import tokenizer as tk
import orjson
import os
import math

# IMPORTANT: IF YOU ARE RUNNING INTO MEMORY ISSUES WE NEED TO SWITCH BACK TO JSON INSTEAD OF ORJSON!!!!!!!
all_ranges = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z']
id_path = "id_to_url.json"
doc_count = 30308


class QueryMachine:
    def __init__(self):
        self.inverted_indexes = {}  # dictionary of our needed dictionaries
        self.id_to_url = open_inverted(id_path)  # Load once

    def retrieveURLS(self, query):
        query_tokens = tk.tokenize_query(str(query))
        doc_ids = self.query_document_match(query_tokens)
        ranked = self.ranking(query_tokens, doc_ids)
        return self.geturls([doc_id for doc_id, _ in ranked])

    def query_document_match(self, query_tokens) -> list:
        intersection_queue = []
        for token in query_tokens:
            bucket = token[0]
            if bucket not in self.inverted_indexes:
                # extract snipit of inverted index as needed
                self.inverted_indexes[bucket] = open_inverted(bucket)

            if token in self.inverted_indexes[bucket]:  # making sure token exists
                intersection_queue.append(set(self.inverted_indexes[bucket][token].keys()))
            else:
                return []  # No results found, automatically fails query match

        intersection_queue.sort(key=len)
        intersection = intersection_queue[0]
        for i in range(1, len(intersection_queue)):
            intersection = self.intersect(intersection, intersection_queue[i])

        return intersection

    @staticmethod
    def intersect(term_list1, term_list2):
        # TEMP CODE UNTIL WE CAN FIX SORTED INTERSECTION
        intersection_set = set(term_list1) & set(term_list2)
        intersection_list = list(intersection_set)
        intersection_list.sort()
        return intersection_list

    def geturls(self, id_list):
        return [self.id_to_url[doc_id][0] for doc_id in id_list if doc_id in self.id_to_url]

    # FORMULA: (1 + log(tf)) * log(N/df)
    def calc_score(self, term, docid):
        bucket = term[0]
        term_frq = self.inverted_indexes[bucket][term][docid]
        term_oc = len(self.inverted_indexes[bucket][term])
        return (1 + math.log(term_frq)) * math.log(doc_count / term_oc)

    # returns top 5, ordered (by score) doc_ids to retrieve
    def ranking(self, query_tokens, doc_ids):
        score_max = 0   # contains max score seen so far.
        token_max = [0] * len(query_tokens)  # list of tuples containing token : max score (of that term)
        # CUT DOWN FOR FASTER PROCESSING
        threshold = 50  # counts down until we've reached 50 "suitable" documents (UPDATE GIVEN TIME)
        ranked_doc_ids = []

        # Go down the list is depleted or pulled 20 worthwhile documents
        for doc in doc_ids:
            if threshold == 0:
                break

            doc_score = 0
            skip_doc = False

            for i, token in enumerate(query_tokens):
                tfidf = self.calc_score(token, doc)
                potential = self.potential_max(token_max[i+1:])

                if (doc_score + tfidf + potential) < score_max:
                    skip_doc = True
                    break
                elif tfidf > token_max[i]:
                    token_max[i] = tfidf

                doc_score += tfidf
            # Only reaches this point if it was worth storing
            if not skip_doc:
                ranked_doc_ids.append((doc, doc_score))
                threshold -= 1
            if doc_score > score_max:
                score_max = doc_score

        ranked_doc_ids.sort(key=lambda x: x[1], reverse=True)
        return ranked_doc_ids  # return top whatever results, print cuts off to top 5

    # Passes in score UP UNTIL that point
    @staticmethod
    def potential_max(token_max):
        max_score = 0
        for score in token_max:
            max_score += score
        return max_score


def open_inverted(token):
    starting_char = token[0]
    if token == id_path:  # opening id_to_url
        with open(token, "rb") as file:
            return orjson.loads(file.read())

    for start in all_ranges:  # opening any of our inverted indexes
        if start == starting_char:
            filename = f"inverted_index_{start}.json"
            if os.path.exists(filename):
                with open(filename, "rb") as file:
                    return orjson.loads(file.read())
            break
    # somehow wasn't found, shouldn't happen
    return {}


def intersect(term_list1, term_list2):
    # TEMP CODE UNTIL WE CAN FIX SORTED INTERSECTION
    intersection_set = set(term_list1) & set(term_list2)
    intersection_list = list(intersection_set)
    intersection_list.sort()
    return intersection_list
