from Esercizio3Intracorso.due_otto_tree import SortedTableMap

# algorithm complexity: O (n^2), reached in the while starting on line 42 and calling a function that executes a for
# loop. In the worst case, the while and for cycle through the SortedTableMap containing as keys, the keys of the nodes
# and as values, the number of values between c1 and c2 that each node possesses.

# The Greedy solution in this case is always optimal because it allows me to take the least number of nodes that cover
# (k, c1, c2). There could not be a situation where you could take advantage of not choosing the great venue.
# Example for absurdity:
#     Node 1 -> 10 values between c1 and c2
#     Node 2 -> 2 values between c1 and c2
#     Node 3 -> 1 value between c1 and c2
# For k = 1, Greedy finds the solution in Node 3 and returns 1 as the number of nodes -> global optimum.
# For k = 2, Greedy finds the solution in Node 2 and returns 1 as the number of nodes -> global optimum.
# For k > 2 and k < 11, Greedy finds the solution in Node 1 and returns 1 as the number of nodes -> global optimum.
# For k = 11, Greedy finds the solution in Node 1 and Node 3 and returns 2 as the number of nodes -> global optimum.
# For k = 12, Greedy finds the solution in Node 1 and Node 2 and returns 2 as the number of nodes -> global optimum.
# For k = 13, Greedy finds the solution in Node 1, Node 2 and Node 3 and returns 3 as the number of nodes -> global optimum.
# For k > 13, None is returned as there are no elements that reach k between c1 and c2 in the example considered.

def cover(tree, k, c1, c2):
    """
    :param tree: (2,8)-Tree saving Currency objects
    :param k: minimum number of currencies requested in between c1 and c2
    :param c1: currency code -> lower limit
    :param c2: currency code  -> upper limit
    :return: num_nodes -> minimum number of nodes that contain k currencies between c1 and c2; it may return None if
            doesn't exists such a cover (k, c1, c2)
    """
    if c1 > c2:
        return "c2 must be greater than c1"

    # Given the configuration adopted for the (2, 8)-Tree in the first test, it was necessary to create three new
    # methods: greatSearch(), greatSearch2(), greatSearch3(). These methods perform a search of all the SortedTableMaps
    # present in each node of the tree and in the "_child" field of each "_Item" present in each SortedTableMap.
    # Calling the "greatSearch" method, to which the currency codes representing lower limit and upper limit are passed
    # as parameters, a single SortedTableMap will be returned ("bigSorted" in this code). This will contain as key all the
    # currency codes present in the tree and included between lower limit and upper limit (c1 and c2), and as value, the
    # minimum key of the respective SortedTableMap to which each currency code belong.
    bigSorted = tree.greatSearch(c1,c2)

    # Now in "bigSorted" we have all the elements between c1 and c2 and also any other elements that belonged to the
    # nodes c1, c2 were part of (not only nodes related to c1 and c2 but also all the SotredTableMaps in which all the
    # currency codes between c1 and c2 were part of). So, now we can delete the values not included between c1 and c2.
    listOfCurrencyCodesToBeDeleted = []
    for currencyCode in bigSorted:
        if currencyCode < c1 or currencyCode > c2:
            listOfCurrencyCodesToBeDeleted.append(currencyCode)
    for currencyCodeToDelete in listOfCurrencyCodesToBeDeleted:
        bigSorted.__delitem__(currencyCodeToDelete)

    # Now in listSorted we have all the elements that we are interested in analyzing.
    # We create a new SortedTableMap (sortedCount) that will contain as keys the minimum keys of the SortedTableMaps of
    # the tree (only those keys who are in "bigSorted") and as values the number of elements (variable "count" in the
    # code) that that SortedTableMap has between c1 and c2.
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

    # Now we have sortedCount which contains the keys and number of values between c1 and c2 (variable "count" in method
    # "getMax") that fall under the SortedTableMap in question. We make a Greedy choice until we cover k elements. If k
    # doesn't even reach it with all the elements between c1 and c2, we return None.
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
