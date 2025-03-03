import queryProcessor as qp


def main():
    # start pre-loading the inverted indexes?
    # keeps running queries until user says stop
    while(True):
        user_q = input("ASK PETE: ")

        # Retrieving valid urls
        id_list = qp.query_document_match(user_q)
        urls = qp.retrieve_urls(id_list)
        pretty_print(urls)

        run_flag = input("\nSearch Again (Y/N)?: ")
        if run_flag[0].lower() == 'n':
            break
    print("Goodbye!")

def pretty_print(urls):
    if len(urls) == 0:
        print("No URLs found")
    else:
        for i in range(min(len(urls), 5)):
            print(f"{i+1}: {urls[i]}")


if __name__ == "__main__":
    main()
