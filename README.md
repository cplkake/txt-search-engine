# txt-search-engine

search_engine.py:
Builds indices of words from txt files, including the count and position of the word in the file.
The search engine then identifies the most relevant txt files given a search query by returning a ranked order of the filenames based on how many times each word in the query appears in each txt file.
Index implemented using a self-balancing binary search tree.
The indices are then stored in a heap-based implementation of a Priority Queue.

processQueries.py:
Implementation of the search engine.
Takes a folder path as input to build the heap of indices, a query file and prints out the matching filenames in order of relevance.
