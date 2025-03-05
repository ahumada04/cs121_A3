import queryProcessor as qp
import time

def main():
    # start pre-loading the inverted indexes?
    # keeps running queries until user says stop
    while(True):
        user_q = input("ASK PETE: ")

        start_time = time.time()
        # Retrieving valid urls
        id_list = qp.query_document_match(user_q)
        urls = qp.retrieve_urls(id_list)
        pretty_print(urls)

        elapsed = (time.time() - start_time) * 1000
        print(f"Query processing took {elapsed:.2f}ms")
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
