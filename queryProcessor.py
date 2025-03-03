import tokenizer as tk
import orjson
# IMPORTANT: IF YOU ARE RUNNING INTO MEMORY ISSUES WE NEED TO SWITCH BACK TO JSON INSTEAD OF ORJSON!!!!!!!

index_path = "inverted_index.json"
id_path = "id_to_url.json"
doc_count = 53194


def query_document_match(query) -> list:
    query_tokens = tk.tokenize(query)
    intersection_queue = []

    # !!!!! IF RUNNING INTO MEMORY ISSUES REFER TO LINE 3 !!!!!
    for token in query_tokens:
        starting_char = token[0]
        if "0" <= starting_char <= "9":
            with open("inverted_index_path_0_9.json", "rb") as file:
                inverted_index = orjson.loads(file.read())
            if token in inverted_index:
                intersection_queue.append(list(inverted_index[token].keys()))
            else:
                return []
        elif "a" <= starting_char <= "h":
            with open("inverted_index_path_a_h.json", "rb") as file:
                inverted_index = orjson.loads(file.read())
            if token in inverted_index:
                intersection_queue.append(list(inverted_index[token].keys()))
            else:
                return []

        elif "i" <= starting_char <= "q":
            with open("inverted_index_path_i_q.json", "rb") as file:
                inverted_index = orjson.loads(file.read())
            if token in inverted_index:
                intersection_queue.append(list(inverted_index[token].keys()))
            else:
                return []
        else:
            with open("inverted_index_path_r_z.json", "rb") as file:
                inverted_index = orjson.loads(file.read())
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


# def calc_score(term, docid):

