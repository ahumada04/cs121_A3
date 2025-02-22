import invertedIndex
import hasher


def main():
    simhash = hasher.SimHash()
    indexer = invertedIndex.Indexer(simhash)
    indexer.traverse("DEV")


if __name__ == "__main__":
    main()
