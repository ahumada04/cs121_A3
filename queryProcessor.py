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
doc_count = 53194


def query_document_match(query) -> list:
    query_tokens = set(tk.tokenize(query))
    intersection_queue = []

    # !!!!! IF RUNNING INTO MEMORY ISSUES REFER TO LINE 3 !!!!!
    for token in query_tokens:
        inverted_index = open_inverted(token)
        if token in inverted_index:
            intersection_queue.append(list(inverted_index[token].keys()))
        else:
            return []

    intersection_queue = sorted(intersection_queue, key=lambda item: len(item))
    intersection = intersection_queue[0]
    for i in range(1, len(intersection_queue)):
        intersection = intersect(intersection, intersection_queue[i])

    return intersection


def intersect(term_list1, term_list2):
    # TEMP CODE UNTIL WE CAN FIX SORTED INTERSECTION
    intersection_set = set(term_list1) & set(term_list2)
    intersection_list = list(intersection_set)
    intersection_list.sort()
    return intersection_list
    # answer = []
    # i = 0
    # j = 0
    # print(f"Intersecting lists of lengths {len(term_list1)} and {len(term_list2)}")
    # while i < len(term_list1) and j < len(term_list2):
    #     if term_list1[i] == term_list2[j]:
    #         answer.append(term_list1[i])
    #         i += 1
    #         j += 1
    #     elif term_list1[i] > term_list2[j]:
    #         j += 1
    #     else:
    #         i += 1
    # print(f"Intersection result: {len(answer)} common IDs")
    # return answer


def retrieve_urls(id_list):
    retrieved_urls = []

    # could pre_load the id_to_url if strapped for time
    with open(id_path, "rb") as file:
        url_map = orjson.loads(file.read())

    # if desperate for time, we could process as an ordered list for O(N) time.
    for id in id_list:
        if id in url_map:
            retrieved_urls.append(url_map[id][0])
    
    return retrieved_urls


# Opens the appropriate inverted index given a token
def open_inverted(token):
    starting_char = token[0].lower()

    for start in all_ranges:
        if start == starting_char:
            filename = f"inverted_index_{start}.json"
            if os.path.exists(filename):
                with open(filename, "rb") as file:
                    return orjson.loads(file.read())
            break
    # somehow wasn't found, shouldn't happen
    return {}


# FORMULA: tf * log(doc_count/ term_occurrence)
def calc_score(term, docid):
    inverted = open_inverted(term)
    term_frq = inverted[term][docid]
    term_oc = len(inverted)

    return term_frq * math.log(doc_count / term_oc)


# returns top 5, ordered (by score) doc_ids to retrieve
# Utaliz
# pass in query tokens, doc_ids,
# list of inverted indexes needed (to avoid unesscarry openings)
def ranking(query_tokens, doc_ids):
    score_max = 0   # contains max score seen so far.
    token_max = [0] * (len(query_tokens) + 1)  # list of tuples containing token : max score (of that term)
    threshold = 20  # counts down until we've reached 20 "suitable documents (UPDATE GIVEN TIME)
    ranked_doc_ids = []
    # Go down the list is depleted or pulled 20 worthwhile documents
    for doc in doc_ids:
        if(threshold == 0):
            break

        doc_score = 0
        skip_doc = False

        for i, token in enumerate(query_tokens):
            tfidf = calc_score(token, doc)
            potential = potential_max(token_max[i+1:])

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
    sorted_rank = ranked_doc_ids.sort(key=lambda x: x[1], reverse=True)
    return sorted_rank[:5]


# calculates the hypothetical best score from a query starting point.
# PASS IN ONLY THE SCORE UP TO THAT POINT
def potential_max(token_max):
    max_score = 0
    for score in token_max:
        max_score += score
    return max_score
