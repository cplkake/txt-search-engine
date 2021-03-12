# code uploaded to github.com/cplkake/txt-search-engine

from os import listdir
from os.path import isfile, join
from assignment2question2 import WebPageIndex, WebpagePriorityQueue

# loads the "webpages" by taking a folder path as input and
# returning a list of WebPageIndex instances taht represent the txt files
def readFiles(path):
    files = [path+'/'+f for f in listdir(path) if isfile(join(path, f))]

    wpiList = []
    for file in files:
        wpiInstance = WebPageIndex(file)
        wpiList.append(wpiInstance)

    return wpiList

# returns the file path for the queries (based on the user input) as a list of string
# output is a list of strings, each line being a singe query
def getQueryFilePath():
    file = input("Please enter the path for the query file: ")
    return open(file).read().split('\n')


# prints to the console the order of ranking from the WebpagePriorityQueue
# only returns the results of the query that had matches
def printResults(webpage_results, query):
    print("\nFor the query: ", query)
    print("The txt files that best match the query are: \n")
    while (webpage_results.peek() is not None) and (webpage_results.peek().value != 0):
        print("{}".format(webpage_results.poll().file))


# given a query file, create a WebpagePriorityQueue instance to process the the queries
# in the query file. For each subsequent query the WebpagePriorityQueue instance is reheaped
# output: prints out the matching filenames from best to worst just like a search engine
def main():

    # retrieves the query file as a list of strings
    queries = getQueryFilePath()

    # calls the readFiles function which creates a list of WebPageIndex instances for each txt file in the folder
    path = input("Please enter the folder path for the txt files: ")
    wpiList = readFiles(path)

    # creates a WebpagePriorityQueue instance from the first query t
    webpage_results = WebpagePriorityQueue(queries[0], wpiList)

    # prints the result of the first query
    printResults(webpage_results, queries[0])

    # process each subsequent query in the query file by creating a WebpagePriorityQueue instance and print the results
    for query in queries[1:]:
        if query != '':
            webpage_results.reheap(query)
            printResults(webpage_results, query)


if __name__ == "__main__":
    main()
