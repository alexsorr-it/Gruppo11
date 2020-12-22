from Esercizio2Intracorso.Currency import Currency
from StruttureDati.graphs.graph import Graph
from math import exp

def cycleDFS(G, v, S, outerList):
    """
    :param G: graph
    :param v: vertex
    :param S: list passed by "arbitrageOpportunity" function; it stores all vertices visited
    :param outerList: list passed by "arbitrageOpportunity" function; it stores lists of cycles
    :return: outerList
    """
    v.setLabel("VISITED")
    S.append(v)
    for e in G.incident_edges(v):
        w = e.opposite(v)
        if w.getLabel() == "UNEXPLORED":
            e.setLabel("DISCOVERY")
            cycleDFS(G, w, S, outerList)
        elif e.getLabel() == "UNEXPLORED":
            #found cycle!
            print(e.element(), e.endpoints()[0].element()._Code, e.endpoints()[1].element()._Code)
            e.setLabel("BACK")
            T = []
            T.append(w)
            count = 1  # auxiliary variable to take elements from list S
            while True:
                o = S[S.__len__() - count]   # taking list elements from last (at most) to first to every while cycle, until a base condition is found
                T.append(o)
                count += 1
                if o == w:
                    check = 0
                    for innerList in outerList:
                        if innerList == T:
                             check += 1
                    if check == 0:
                        outerList.append(T[::-1])  # need reversed list because elements in S are stored in right order and, since we get them from last (at most) to first, we have to restore the initial order by doing this operation
                    break
                elif S.__len__() - count < 0:
                    break
    S.remove(v)
    return outerList

def arbitrageOpportunity(C, s):
    """
    :param C: set of Currency objects (we have supposed it is a list)
    :param s: a currency object
    :return: returnList -> list of strings who represent all information deemed necessary; this function may also return "None"
    """
    G = Graph(directed=True)
    v = None

    # setting Currency objects as vertex of the graph and getting vertex 'v' corresponding to Currency object 's'
    for currency in C:
        if currency == s:
            v = G.insert_vertex(x=currency)
        else:
            G.insert_vertex(x=currency)

    # checking the validity of v
    try:
        G._validate_vertex(v)
    except ValueError:
        return None
    except TypeError:
        return None

    # setting edges between vertex
    for vertex1 in G.vertices():
        for vertex2 in G.vertices():
            try:
                if vertex1 != vertex2 and vertex1.element()._Changes.__getitem__(vertex2.element()._Code) is not None:
                    G.insert_edge(vertex1, vertex2, x=vertex1.element()._Changes.__getitem__(vertex2.element()._Code))
            except KeyError:
                pass

    # getting vertex with max number of incident edges
    max = G.degree(v, False)
    vref = v
    for ver in G.vertices():
        if max < G.degree(ver, False):
            max = G.degree(ver, False)
            vref = ver

    cycles = cycleDFS(G, vref, [], [])   # search for all cycles in the graph constructed
    if cycles.__len__() == 0:
        return False
    else:
        countCycle = 0
        returnList = []
        for oneCycle in cycles:
            sumEdge = 0
            if v in oneCycle:
                countCycle += 1
                cycleDescription = "cycle n°" + str(countCycle) + ":"
                simpleCycle = []
                for index in range(0, oneCycle.__len__()-1):
                    arco = G.get_edge(oneCycle[index], oneCycle[index+1])
                    sumEdge += arco.element()
                    if index < oneCycle.__len__()-1:
                        simpleCycle.append(str(oneCycle[index].element()._Code))
                concatCycle = simpleCycle + simpleCycle
                adjustCycle = []
                count = 0   # variable for checking elements of the cycle
                for currencyCode in concatCycle:
                    if currencyCode == v.element()._Code:
                        count += 1
                    if count == 1:
                        adjustCycle.append(currencyCode)
                adjustCycle.append(v.element()._Code)   # closing cycle with currency code passed in input to the function as currency object 's'
                for rightCurrencyCode in range(0, adjustCycle.__len__()):
                    if rightCurrencyCode == 0:
                        cycleDescription = cycleDescription + " (" + str(adjustCycle[rightCurrencyCode]) + ","
                    elif rightCurrencyCode == adjustCycle.__len__() - 1:
                        cycleDescription = cycleDescription + " " + str(adjustCycle[rightCurrencyCode]) + ")"
                    else:
                        cycleDescription = cycleDescription + " " + str(adjustCycle[rightCurrencyCode]) + ","
                if sumEdge >= 0:
                    cycleDescription = cycleDescription + "." + " Final rate exchange: " + str(sumEdge) + ". False"
                else:
                    cycleDescription = cycleDescription + "." + " Final rate exchange: " + str(sumEdge) + ". By exchanging 1 " + v.element()._Code + ", one receives " + str(exp(-sumEdge)) + " " + v.element()._Code + "."
                returnList.append(cycleDescription)
    return returnList

# ----------CURRENCY INITIALIZATION-----------#
currUSD = Currency("USD")
currEUR = Currency("EUR")
currGBP = Currency("GBP")

#--------------CHANGES--------------#
currUSD.addChange("EUR", 0.1)
currEUR.addChange("GBP", -0.31)
currGBP.addChange("USD", 0.005)
currEUR.addChange("USD", 0.2)
currGBP.addChange("EUR", 0.005)
currUSD.addChange("GBP", 0.3)

C = [currUSD, currEUR, currGBP]   # we have supposed that the set of element containing Currency objects is a list
s = currGBP

# # PROVA CON GRAFO SLIDE 15, 19-DFS
# # ----------CURRENCY INITIALIZATION-----------#
# currAAA = Currency("AAA")
# currBBB = Currency("BBB")
# currCCC = Currency("CCC")
# currDDD = Currency("DDD")
# currEEE = Currency("EEE")
#
# #--------------CHANGES--------------#
# currAAA.addChange("BBB", 0.3)
# currAAA.addChange("CCC", 0.3)
# currAAA.addChange("DDD", 0.3)
# currBBB.addChange("DDD", -0.31)
# currCCC.addChange("DDD", 0.005)
# currCCC.addChange("EEE", 0.005)
# currDDD.addChange("EEE", -0.31)
# currEEE.addChange("AAA", 0.005)
#
# C = [currAAA, currBBB, currCCC, currDDD, currEEE]   # we have supposed that the set of element containing Currency objects is a list
# s = currEEE

#-------------TESTING ARBITRAGE OPPORTUNITY-----------#
lista = arbitrageOpportunity(C, s)
if isinstance(lista, list):
    for i in lista:
        print(i)
else:
    print(lista)