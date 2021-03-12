# code uploaded to github.com/cplkake/txt-search-engine

class AVLnode:
    def __init__(self, key, value):
        self.left = None
        self.right = None
        self.key = key
        self.value = value
        self.height = 0


class AVLTreeMap:
    # creates a root node when an AVLTreeMap is instantiated (even if no values as input)
    def __init__(self, key=None, value=None):
        self.root = AVLnode(key, value)

    # wrapper function for rec_get() that returns the value for a given key in the tree
    # returns the value for a given key if it exists in the tree
    def get(self, key):
        value = self.rec_get(self.root, key)
        return value

    # returns the value if the given key exists in the AVL tree
    # returns None if the key is not in the tree
    def rec_get(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node.value
        elif key < node.key:
            value = self.rec_get(node.left, key)
        elif key > node.key:
            value = self.rec_get(node.right, key)
        return value

    # wrapper function for avl_insert() which does the grunt work of
    # inserting a new key-value pair and doing the necessary adjustments
    # to maintain a valid AVL tree
    def put(self, key, value):
        self.root = self.avl_insert(self.root, key, value)

    # inserts the specified key-value pair into the proper position in the tree
    # updates the height of the affected sub-trees and carries out the necessary rotations
    # if the balance factor of the sub-trees are out of order
    def avl_insert(self, node, key, value):
        if node is None or node.key is None:
            if isinstance(value, str):               # if value is a string, stores it directly in the value attribute
                return AVLnode(key, value)
            else:                                    # otherwise stores the new value in a list
                return AVLnode(key, [value])
        elif key < node.key:
            node.left = self.avl_insert(node.left, key, value)
        elif key > node.key:
            node.right = self.avl_insert(node.right, key, value)
        else:                                        # if key == node.key (used for when storing strings as keys)
            node.value.append(value)

        left_height = self.getHeight(node.left)
        right_height = self.getHeight(node.right)

        if left_height > right_height:
            node.height = 1 + left_height
        else:
            node.height = 1 + right_height

        balance = self.getBalance(node)       # self.getBalance() calculates the balance factor for a specified sub-tree

        # case 1: left left imbalance
        if balance < -1 and key < node.left.key:
            return self.rightRotate(node)

        # case 2: right right imbalance
        if balance > 1 and key > node.right.key:
            return self.leftRotate(node)

        # case 3: left right imbalance
        if balance < -1 and key > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        # case 4: right left imbalance
        if balance > 1 and key < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    # returns the height of the specified sub-tree
    def getHeight(self, node):
        if node:
            return node.height
        else:
            return -1

    # calculates and returns the balance factor for a specified sub-tree root node
    def getBalance(self, node):
        return self.getHeight(node.right) - self.getHeight(node.left)

    # performs a right rotation given a grandparent node
    def rightRotate(self, bNode):
        aNode = bNode.left
        beta = aNode.right

        aNode.right = bNode
        bNode.left = beta

        # updates the height of aNode and bNode
        bNode.height = 1 + max(self.getHeight(bNode.left), self.getHeight(bNode.right))
        aNode.height = 1 + max(self.getHeight(aNode.left), self.getHeight(aNode.right))

        return aNode

    # performs a left rotation given a grandparent node
    def leftRotate(self, aNode):
        bNode = aNode.right
        beta = bNode.left

        bNode.left = aNode
        aNode.right = beta

        # updates the height of aNode and bNode
        aNode.height = 1 + max(self.getHeight(aNode.left), self.getHeight(aNode.right))
        bNode.height = 1 + max(self.getHeight(bNode.left), self.getHeight(bNode.right))

        return bNode


# class that will contain the index representation of a web page
class WebPageIndex:
    def __init__(self, file):
        self.file = file        # stores the file path as an attribute
        self.value = 0          # value for ranking based on queries

        # store the contents of the delimited text file as a list of words, removing unnecessary characters
        with open(file, 'r') as f:
            flat_list = [word for line in f for word in line.replace('i.e', 'ie').replace(',', ' ').replace('(', ' ').replace('/', ' ').replace(')', ' ').replace('.', ' ').replace(':', ' ').replace(';', ' ').replace('[1]', ' ').replace('[2]', ' ').replace('[3]', ' ').replace('\"', ' ').replace(':', ' ').replace('-', ' ').lower().split()]

        # initialize an AVLTreeMap object for the input text file
        self.tree_map = AVLTreeMap()

        # iterate through flat_list, storing each word in the AVLTreeMap instance
        for i in range(len(flat_list)):
            self.tree_map.put(flat_list[i], i)

    # returns the number of times s appears in the WebPageIndex instance
    def getCount(self, s):
        result = self.tree_map.get(s)
        if result is None:
            return 0
        else:
            return len(result)


# A maxheap-based implementation of a Priority Queue
# contains an array-based list to hold the data items in the priority queue
class WebpagePriorityQueue:
    # takes a query and a set of WebPageIndex instances as input and
    # create a max heap  with each node in the max heap represents a WebPageIndex instance
    # priority of instances defined by the sum of the word counts of the pages for the words in the query
    def __init__(self, query, wpiList):
        self.query = query
        self.maxHeap = []
        self.wpiList = wpiList

        # calculates the priority of and stores each WebPageIndex from the wpiList into maxHeap
        for wpi in self.wpiList:
            value = 0
            for word in query.split():
                value += wpi.getCount(word)
            wpi.value = value
            self.maxHeap.append(wpi)

            # index values for child and parent
            child = len(self.maxHeap) - 1
            parent = max(int((child - 1) / 2), 0)       # ensures that there is no index value below 0

            # moves the WebPageIndex instance up the heap to its appropriate position
            while self.maxHeap[child].value > self.maxHeap[parent].value:
                temp = self.maxHeap[child]
                self.maxHeap[child] = self.maxHeap[parent]
                self.maxHeap[parent] = temp
                child = parent
                parent = max(int((child - 1) / 2), 0)   # ensures that there is no index value below 0

    # return the WebPageIndex with the highest priority in the WebpagePriorityQueue without removing it
    def peek(self):
        if len(self.maxHeap) != 0:
            return self.maxHeap[0]
        else:
            return None

    # remove and return the WebPageIndex with the highest priority in the WebpagePriorityQueue instance
    def poll(self):
        if len(self.maxHeap) == 0:          # situation when heap is empty
            return None
        else:
            root = self.maxHeap[0]
            if len(self.maxHeap) == 1:      # situation when heap is of length 1
                del self.maxHeap[0]
                return root
            else:                           # situation when heap length is longer than 1
                # removes the right-most node in the bottom-most row and moves it to the top
                self.maxHeap[0] = self.maxHeap[-1]
                del(self.maxHeap[-1])

                parent = 0
                child1 = min(2 * parent + 1, len(self.maxHeap) - 1)  # ensures child index values stay within the bounds
                child2 = min(2 * parent + 2, len(self.maxHeap) - 1)

                # moves the top WebPageIndex instance down the heap to its appropriate position
                while self.maxHeap[parent].value < self.maxHeap[child1].value or self.maxHeap[parent].value < self.maxHeap[child2].value:
                    # switch parent instance with the child that has the higher value
                    if self.maxHeap[child1].value > self.maxHeap[child2].value:
                        temp = self.maxHeap[child1]
                        self.maxHeap[child1] = self.maxHeap[parent]
                        self.maxHeap[parent] = temp
                        parent = child1
                        child1 = min(2 * parent + 1, len(self.maxHeap) - 1)  # ensures child index values stay within the bounds
                        child2 = min(2 * parent + 2, len(self.maxHeap) - 1)
                    else:
                        temp = self.maxHeap[child2]
                        self.maxHeap[child2] = self.maxHeap[parent]
                        self.maxHeap[parent] = temp
                        parent = child2
                        child1 = min(2 * parent + 1, len(self.maxHeap) - 1)  # ensures child index values stay within the bounds
                        child2 = min(2 * parent + 2, len(self.maxHeap) - 1)
                return root

    # takes a new query input and re-heaps the WebpagePriorityQueue making use of tempHeap
    def reheap(self, query):
        self.maxHeap = []           # fresh start

        # calculates the priority of and stores each WebPageIndex from the wpiList into maxHeap
        for wpi in self.wpiList:
            value = 0
            for word in query.split():
                value += wpi.getCount(word)
            wpi.value = value
            self.maxHeap.append(wpi)

            # index values for child and parent
            child = len(self.maxHeap) - 1
            parent = max(int((child - 1) / 2), 0)       # ensure the parent index value is within the bounds of the heap

            # moves the WebPageIndex instance up the heap to its appropriate position
            while self.maxHeap[child].value > self.maxHeap[parent].value:
                temp = self.maxHeap[child]
                self.maxHeap[child] = self.maxHeap[parent]
                self.maxHeap[parent] = temp
                child = parent
                parent = max(int((child - 1) / 2), 0)   # ensure the parent index value is within the bounds of the heap


def main():
    # test key-value pairs
    testDict = {15: "bob",
                20: "anna",
                24: "tom",
                10: "david",
                13: "david",
                7: "ben",
                30: "karen",
                36: "erin",
                25: "david"}

    test_tree = AVLTreeMap()

    # insert each key-value pair in testDict into the AVLTreeMap instance
    for key, value in testDict.items():
        test_tree.put(key, value)


if __name__ == "__main__":
    main()
