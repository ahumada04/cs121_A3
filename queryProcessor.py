import tokenizer as tk
import json


index_path = "inverted_index.json"
id_path = "id_to_url.json"


def query_document_match(query) -> list:
    query_tokens = tk.tokenize(query)
    intersection_queue = []

    with open(index_path, "r") as file:
        inverted_index = json.load(file)

    for token in query_tokens:
        if token in inverted_index:
            intersection_queue.append(list(inverted_index[token].keys()))
        else:
            return []

    intersection_queue = sorted(intersection_queue, key=lambda item: len(item))
    intersection = intersection_queue[0]
    for i in range(1, len(intersection_queue)):
        intersection = intersect(intersection, intersection_queue[i])

    return intersection


@staticmethod
def intersect(term_list1, term_list2):
    answer = []
    i = 0
    j = 0
    while i < len(term_list1) and j < len(term_list2):
        if term_list1[i] == term_list2[j]:
            answer.append(term_list1[i])
            i += 1
            j += 1
        elif term_list1[i] > term_list2[j]:
            j += 1
        else:
            i += 1
    return answer


def retrieve_urls(id_list):
    retrieved_urls = []

    # could pre_load the id_to_url if strapped for time
    with open(id_path, "r") as file:
        url_map = json.load(file)

    # if desperate for time, we could process as an ordered list for O(N) time.
    for id in id_list:
        if id in url_map:
            retrieved_urls.append(url_map[id][0])
    
    return retrieved_urls
            
            
        


