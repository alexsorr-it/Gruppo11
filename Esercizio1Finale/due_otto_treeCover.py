from Esercizio3Intracorso.due_otto_tree import abTree as abt, SortedTableMap
from Esercizio2Intracorso.Currency import Currency

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


#----------ABTREE INITIALIZATION-----------#
albero = abt()

#----------CURRENCY INITIALIZATION AND TREE FILLING-----------#
def inizializing():
    curr1 = Currency("AFN")
    curr2 = Currency("ALL")
    curr3 = Currency("AMD")
    curr4 = Currency("AOA")
    curr5 = Currency("ARS")
    curr6 = Currency("AUD")
    curr7 = Currency("AWG")
    curr8 = Currency("BAM")
    curr9 = Currency("BDD")
    curr10 = Currency("BDT")
    curr11 = Currency("BGN")
    curr12 = Currency("BHD")
    curr13 = Currency("BIF")
    curr14 = Currency("BMD")
    curr15 = Currency("BND")
    curr16 = Currency("BOB")
    curr17 = Currency("BOV")
    curr18 = Currency("BRL")
    curr19 = Currency("BSD")
    curr20 = Currency("BTN")
    curr21 = Currency("BWP")
    curr22 = Currency("BYR")
    curr23 = Currency("BZD")
    curr24 = Currency("CAD")
    curr25 = Currency("CLF")
    curr26 = Currency("CLP")
    curr27 = Currency("CNY")
    curr28 = Currency("CVE")
    curr29 = Currency("DZD")
    curr30 = Currency("EUR")
    curr31 = Currency("INR")
    curr32 = Currency("KHR")
    curr33 = Currency("NOK")
    curr34 = Currency("SAR")
    curr35 = Currency("THB")
    curr36 = Currency("TJS")
    curr37 = Currency("XCD")
    curr38 = Currency("ZWL")

    #------ADDING-------#
    albero.addElement(curr1._Code, 1)
    albero.addElement(curr2._Code, 2)
    albero.addElement(curr3._Code, 3)
    albero.addElement(curr4._Code, 4)
    albero.addElement(curr5._Code, 5)
    albero.addElement(curr6._Code, 6)
    albero.addElement(curr7._Code, 7)
    albero.addElement(curr8._Code, 8)
    albero.addElement(curr9._Code, 9)
    albero.addElement(curr10._Code, 10)
    albero.addElement(curr11._Code, 11)
    albero.addElement(curr12._Code, 12)
    albero.addElement(curr13._Code, 13)
    albero.addElement(curr14._Code, 14)
    albero.addElement(curr15._Code, 15)
    albero.addElement(curr16._Code, 16)
    albero.addElement(curr17._Code, 17)
    albero.addElement(curr18._Code, 18)
    albero.addElement(curr19._Code, 19)
    albero.addElement(curr20._Code, 20)
    albero.addElement(curr21._Code, 21)
    albero.addElement(curr22._Code, 22)
    albero.addElement(curr23._Code, 23)
    albero.addElement(curr24._Code, 24)
    albero.addElement(curr25._Code, 25)
    albero.addElement(curr26._Code, 26)
    albero.addElement(curr27._Code, 27)
    albero.addElement(curr28._Code, 28)
    albero.addElement(curr29._Code, 29)
    albero.addElement(curr30._Code, 30)
    albero.addElement(curr31._Code, 31)
    albero.addElement(curr32._Code, 32)
    albero.addElement(curr33._Code, 33)
    albero.addElement(curr34._Code, 34)
    albero.addElement(curr35._Code, 35)
    albero.addElement(curr36._Code, 36)
    albero.addElement(curr37._Code, 37)
    albero.addElement(curr38._Code, 38)

#----PRINTING RESULTS-----#
inizializing()
n = cover(albero, 10, "ARS", "CLP")
albero.stampa()

#----PRINTING KEYS----#
lista = albero.getKeys()
print("\n\nCHIAVI:\n")
for i in lista:
    print(i)

print("\n\n(k, c1, c2)-cover of T with the minimum number of nodes: ", n)
