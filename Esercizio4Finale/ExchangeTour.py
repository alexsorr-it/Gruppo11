from Esercizio2Intracorso.Currency import Currency
from StruttureDati.graphs.dfs import DFS_exchangeTour
from StruttureDati.graphs.graph import Graph

curr1 = Currency("EUR")
curr2 = Currency("USD")
curr3 = Currency("GBP")
curr4 = Currency("CNY")
curr5 = Currency("JPY")

curr1.addChange("USD", 0.3)
curr2.addChange("EUR", 0.3)
curr1.addChange("GBP", 0.31)
curr3.addChange("EUR", 0.31)
curr2.addChange("GBP", 0.09)
curr3.addChange("USD", 0.09)
curr3.addChange("CNY", 0.05)
curr4.addChange("GBP", 0.05)
curr1.addChange("CNY", 0.87)
curr4.addChange("EUR", 0.87)
curr2.addChange("JPY", 0.43)
curr5.addChange("USD", 0.43)
curr5.addChange("CNY", 0.11)
curr4.addChange("JPY", 0.11)

print("CURR1: ")
print(curr1.toStringChanges())
print("CURR2: ")
print(curr2.toStringChanges())
print("CURR3: ")
print(curr3.toStringChanges())
print("CURR4: ")
print(curr4.toStringChanges())
print("CURR5: ")
print(curr5.toStringChanges())

grafo = Graph(False)

v1 = grafo.insert_vertex(curr1.getCode())
v2 = grafo.insert_vertex(curr2.getCode())
v3 = grafo.insert_vertex(curr3.getCode())
v4 = grafo.insert_vertex(curr4.getCode())
v5 = grafo.insert_vertex(curr5.getCode())


grafo.insert_edge(v1, v2, x=0.3)
grafo.insert_edge(v2, v3, x=0.09)
grafo.insert_edge(v2, v5, x=0.43)
grafo.insert_edge(v1, v3, x=0.31)
grafo.insert_edge(v1, v4, x=0.87)
grafo.insert_edge(v4, v5, x=0.11)
grafo.insert_edge(v3, v4, x=0.05)

listCurrency = {}
exchangeTour = []

def printTour(exchangeTour):
    """
    Print all the currency in the exchange tour.

    :param exchangeTour: a list containing all the currency choosen by DFS algorithm
    """
    print('EXCHANGE TOUR')
    stampa = "("
    for curr in exchangeTour:
        stampa += str(curr) + " , "
    print(stampa + ")")

def checkValidTour(exchangeTour):
    """
    Check if the list passed as parameters is a valid eschange tour, so if respect the following constraints:

    - All currency must be involved in the tour
    - Currencies must be involved only one time
    - Consecutive Currencies must be related by a rate exchange

    :param exchangeTour: a list containing all the currency choosen by DFS algorithm
    """
    for i in range(0, len(exchangeTour) - 1):   # i va da 0 a 4
        if not grafo.get_edge(exchangeTour[i], exchangeTour[i+1]):
            return False
    return True

def makeTour(start_vertex, score):
    """
    Define the exchange tour starting from a vertex which is in a graph.

    :param start_vertex: vertex of the graph from which we want to start DFS algorithm
    :param score: initial score (may be 0)
    :return: score of the exchange tour
    """
    score = DFS_exchangeTour(grafo, start_vertex, start_vertex, listCurrency, exchangeTour, score, 0)
    exchangeTour.append(start_vertex)
    printTour(exchangeTour)
    isValid = checkValidTour(exchangeTour)
    if(isValid):
        print('exchange tour is valid with score ', score)
    else:
        print('exchange tour is not valid')


makeTour(v4, 0)