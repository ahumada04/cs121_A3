import queryProcessor as qp


def main():
    # start pre-loading the inverted indexes?
    print("ASK HERE: ")
    user_q = input()

    # grab list of doc ids that match all tokens in user query
    id_list = qp.query_document_match(user_q)
    foundURLS = qp.retrieve_urls(id_list)

    pretty_print(foundURLS)


def pretty_print(urls):
    if(len(urls) == 0):
        print("No URLs found")
    else:
        for i in range(len(urls)):
            print(f"{i+1}: {urls[i]}")


if __name__ == "__main__":
    main()
