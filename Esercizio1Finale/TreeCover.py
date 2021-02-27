from Esercizio3Intracorso.due_otto_tree import SortedTableMap

# Algorithm complexity: O (k*n), reached in the while loop starting at line 89 which calls a function that executes a
# for loop. The while loop is executed k times and the for loop, in the worst case, iterates through the entire
# SortedTableMap (SortCount, whose length, that we assume to be n, is decreased each time we call "getMax" function)
# containing as keys, the keys of the nodes and as values, the number of elements between c1 and c2 that each node has.

# The Greedy solution in this case is always optimal because it allows to take the least number of nodes that cover
# (k, c1, c2). There could not be a situation where one could take advantage of not choosing the local optimum.
# Example for absurdity:
     # Node 1 -> 10 values between c1 and c2
     # Node 2 -> 2 values between c1 and c2
     # Node 3 -> 1 value between c1 and c2
# For k = 1, Greedy finds the solution in Node 3 and returns 1 as the number of nodes -> local and global optimum.
# For k = 2, Greedy finds the solution in Node 2 and returns 1 as the number of nodes -> local and global optimum.
# For k > 2 and k < 11, Greedy finds the solution in Node 1 and returns 1 as the number of nodes -> local and global optimum.
# For k = 11, Greedy finds the solution in Node 1 and Node 3 and returns 2 as the number of nodes -> local and global optimum.
# For k = 12, Greedy finds the solution in Node 1 and Node 2 and returns 2 as the number of nodes -> local and global optimum.
# For k = 13, Greedy finds the solution in Node 1, Node 2 and Node 3 and returns 3 as the number of nodes -> local and global optimum.
# For k > 13, None is returned since there are no elements reaching k between c1 and c2 in the example considered.

def cover(tree, k, c1, c2):
    """
    :param tree: (2,8)-Tree saving Currency objects
    :param k: minimum number of currencies requested in between c1 and c2
    :param c1: currency code -> lower limit
    :param c2: currency code  -> upper limit
    :return: num_nodes -> minimum number of nodes that contain k currencies between c1 and c2; it may return None if
            doesn't exists such a cover (k, c1, c2)
    """

    if not isinstance(k, int):
        return "k must be integer"

    if not isinstance(c1, str) or not isinstance(c2, str) or not((c1.isupper() and (len(c1) == 3))
                                                                 and (c2.isupper() and (len(c2) == 3))):
        return "keys must be of three upper capital letter"

    if c1 > c2:
        return "c2 must be greater than c1"

    # Checking if c1 and c2 are valid currency
    v1 = tree.search(c1)
    v2 = tree.search(c2)
    if v1 is None or v2 is None:
        return "c1 or c2 are not valid currencies because one or both of them are not part of the constructed tree"

    # Given the configuration adopted for the tree (2, 8) in the first test, it was necessary to create in the Currency
    # class, developed in the first test, three new methods: greatSearch (), greatSearch2 (), greatSearch3 (). These
    # methods perform a search on all the SortedTableMaps present in each node of the tree and in the "_child" field of
    # each "_Item" present in each SortedTableMap.
    # Calling the "greatSearch" method, which is passed as parameters the currency codes representing the lower bound
    # and the upper bound, will return a single SortedTableMap ("bigSorted" in this code). This will contain as key all
    # the currency codes present in the tree and included between the lower limit and the upper limit (c1 and c2), and
    # as a value, the minimum key of the respective SortedTableMap to which each currency code belongs.
    bigSorted = tree.greatSearch(c1,c2)

    # Now in "bigSorted" we have all the elements between c1 and c2 and also all the other elements that belonged to the
    # nodes c1 and c2 were part of (in reality, we are not referring only to the nodes containing c1 and c2, but also to
    # all the SotredTableMaps whose currency codes are between c1 and c2). So, now we can delete from the constructed
    # SortedTableMap, the values not included between c1 and c2.
    listOfCurrencyCodesToBeDeleted = []
    for currencyCode in bigSorted:
        if currencyCode < c1 or currencyCode > c2:
            listOfCurrencyCodesToBeDeleted.append(currencyCode)
    for currencyCodeToDelete in listOfCurrencyCodesToBeDeleted:
        bigSorted.__delitem__(currencyCodeToDelete)

    # Now in bigSorted we have all the elements that we are interested in analyzing. We create a new SortedTableMap
    # (SortCount) which will contain as keys the minimum keys of the SortedTableMaps of the tree that serve as a
    # reference for all the elements belonging to the SortedTableMap (only those keys that are in "bigSorted") and as
    # values the number of elements (variable "count" in your code) that each SortedTableMap has between c1 and c2.
    sortedCount = SortedTableMap()
    alreadyEntered = []
    for currencyCode1 in bigSorted:
        count = 0
        for currencyCode2 in bigSorted:
            if currencyCode2 >= currencyCode1:
                if bigSorted.__getitem__(currencyCode1) == bigSorted.__getitem__(currencyCode2) and \
                        currencyCode2 not in alreadyEntered:  # identity on the keys
                    count += 1
                    alreadyEntered.append(currencyCode2)
                    sortedCount.__setitem__(bigSorted.__getitem__(currencyCode1), count)

    # We now have SortCount which contains the keys and number of values between c1 and c2 (variable "count" in the
    # "getMax" method) that fall into the SortedTableMap in question. We make a greedy choice until we cover k elements.
    # If k doesn't even reach it with all the elements between c1 and c2, we return None.
    num_nodes = 0
    while k > 0:
        num_nodes += 1  # we update the number of nodes needed
        max = getMax(sortedCount)
        k = k - max
        if k <= 0:
            return num_nodes
        elif sortedCount.__len__() == 0:
            return None

def getMax(sortedCount):
    max = 0
    maxKey = 0
    for currencyCode in sortedCount:
        count = sortedCount.__getitem__(currencyCode)   # number of currency codes between c1 and c2 and related to
                                                        # current SortedTableMap identified by "currencyCode"
        if max <= count:
            max = count
            maxKey = currencyCode
    sortedCount.__delitem__(maxKey)
    return max
