import re
#  DO NOT DELETE
#  TBD, might not parse out stop words for this assignment
# STOP_WORDS = [
#     "s", "ve", "d", "ll", "t",
#     "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at",
#     "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "cannot", "could",
#     "did", "do", "does", "doing", "down", "during", "each", "few", "for",
#     "from", "further", "had", "has", "have", "having", "he",
#     "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
#     "if", "in", "into", "is", "it", "its", "itself", "me", "more", "most",
#     "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
#     "ourselves", "out", "over", "own", "same", "she", "should",
#     "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there",
#     "these", "they", "this", "those", "through", "to", "too",
#     "under", "until", "up", "very", "was", "we", "were", "what",
#     "when", "where", "which", "while", "who", "whom", "why", "with",
#     "would", "you", "your", "yours", "yourself", "yourselves"]


def tokenize(content: str) -> list:
    if not content:
        return []
    else:
        pattern = r"[a-zA-Z0-9]+"
    # UPDATE LATER TO READ BY BYTE INSTEAD OF ALL AT ONCE
        token_list = re.findall(pattern, content.lower())
        return token_list


def computeWordFrequencies(token_list: list) -> dict:
    token_dict = {}

    for token in sorted(token_list):
        if token in STOP_WORDS:
            continue
        elif token in token_dict:
            token_dict[token] += 1
        else:
            token_dict[token] = 1

    return dict(sorted(token_dict.items(), key=lambda item: item[1], reverse=True))
