from StruttureDati.graphs.graph import Graph
from Esercizio2Intracorso.Currency import Currency


def dfs(graph, start, end):
    margin = [(start, [])]
    while margin:
        state, path = margin.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            margin.append((next_state, path+[next_state]))

def constructingGraph(G):

    graph = {}
    listVertex = []

    for vertex in G.vertices():
        for edge in G.edges():
            try:
                other = edge.opposite(vertex)
                listVertex.append(other)
            except ValueError:
                pass
        graph.__setitem__(vertex, listVertex)
        listVertex = []

    allCycles = [[node] + path for node in graph for path in dfs(graph, node, node)]

    cycles = []
    for cycle in allCycles:
        #aggiungo solo i cicli che includono tutti i vertici del grafo
        if len(cycle) - 1 == len(G.vertices()):
            cycles.append(cycle)
    return cycles

def callFirst(C):
    G = Graph(directed=False)

    for currency in C:
        G.insert_vertex(x=currency)

    # setting edges between vertex
    for vertex1 in G.vertices():
        for vertex2 in G.vertices():
            try:
                if vertex1 != vertex2 and vertex1.element()._Changes.__getitem__(vertex2.element()._Code) is not None:
                    G.insert_edge(vertex1, vertex2, x=vertex1.element()._Changes.__getitem__(vertex2.element()._Code))
            except KeyError:
                pass

    cycles = constructingGraph(G)
    listSum = []
    listProvv = []
    for listCycle in cycles:
        sum = 0
        for index in range(0, len(listCycle) - 1):
            edge = G.get_edge(listCycle[index], listCycle[index + 1])
            sum = sum + edge.element()
            listProvv.append(listCycle[index].element()._Code)
            if index == len(listCycle) - 2:
                listProvv.append(listCycle[index + 1].element()._Code)
        listSum.append([listProvv,sum])
        listProvv = []

    return listSum

def localSearch(cyclesAndSum):
    """
    Local search Algorithm
    - We mantain the current solution S
    - We mantain the current best solution S*
    - We choose a solution S' in N(S)
    - We set S' as the new current solution
    - If c(S') <= c(S*), we set S' as the current best solution
    - Repeat

    :param exchangeTour: a list containing all the currency choosen by DFS algorithm
    :param count: Energy of the problem, such as the cost function to minimize
    :return: Best configuration and its cost
    """

    #currentBestSolution = []
    #score = -1
    print('\n\nLOCAL SEARCH')
    #Neighbour-hood relation (two solution differ from each other by the start vertex choosen for the DFS algorithm)
    # for cas in cyclesAndSum:
    #     current_score = cas[1]
    #     if current_score < score and current_score > 0 or score == -1:
    #         score = current_score
    #         currentBestSolution = cas[0]

    score = cyclesAndSum[0][1]
    currentBestSolution = cyclesAndSum[0][0]
    index = 0
    while index < len(cyclesAndSum):
        current_score = cyclesAndSum[index][1]
        if current_score < score and current_score > 0:
            score = current_score
            currentBestSolution = cyclesAndSum[index][0]
        index += 1

    print('\nBEST SOLUTION ', currentBestSolution)
    print('SCORE ', score)


#------------MAIN-----------------------#

curr1 = Currency("EUR")
curr2 = Currency("USD")
curr3 = Currency("GBP")
curr4 = Currency("CNY")
curr5 = Currency("JPY")
curr6 = Currency("OZZ")
curr7 = Currency("LEE")
curr8 = Currency("LAS")
curr9 = Currency("AAA")
curr10 = Currency("GNE")

curr11 = Currency("TOP")
curr12 = Currency("LAA")
curr13 = Currency("ANA")
curr14 = Currency("IMI")
curr15 = Currency("AVE")
curr16 = Currency("TRE")
curr17 = Currency("ROO")
curr18 = Currency("OOO")


#--------INPUT TRACCIA------#
curr1.addChange("USD", 0.3)
curr1.addChange("GBP", 0.31)
curr2.addChange("GBP", 0.09)
curr3.addChange("CNY", 0.05)
curr1.addChange("CNY", 0.87)
curr2.addChange("JPY", 0.43)
curr5.addChange("CNY", 0.11)
curr6.addChange("USD", 0.23)
curr6.addChange("LEE", 0.63)
curr7.addChange("EUR", 0.50)
curr7.addChange("CNY", 0.61)
curr8.addChange("OZZ", 0.82)
curr8.addChange("AAA", 0.21)
curr9.addChange("JPY", 0.87)
curr9.addChange("GNE", 0.57)
curr10.addChange("JPY", 0.44)

curr10.addChange("ANA", 0.20)
curr10.addChange("TOP", 0.10)
curr11.addChange("ANA", 0.30)
curr11.addChange("JPY", 0.20)
curr11.addChange("CNY", 0.40)
curr11.addChange("LAA", 1.20)
curr12.addChange("CNY", 0.70)
curr12.addChange("IMI", 0.50)
curr14.addChange("CNY", 0.80)
curr14.addChange("OOO", 0.50)
curr14.addChange("ROO", 0.90)
curr18.addChange("ROO", 2.40)
curr17.addChange("AVE", 0.30)
curr17.addChange("TRE", 0.40)
curr16.addChange("AVE", 1.40)
curr15.addChange("LEE", 0.9)

#-------------TESTING ARBITRAGE OPPORTUNITY-----------#
C = [curr2, curr1, curr3, curr4, curr5, curr6,
     curr7, curr8, curr9, curr10, curr11, curr12,
     curr13, curr14, curr15, curr16, curr17, curr18]   # we have supposed that the set of element containing Currency objects is a list
cyclesAndSum = callFirst(C)
print("Exchange tour\t\t\t\t\t\t\t\t Rates\n")
for cas in cyclesAndSum:
    print(cas)


print(len(cyclesAndSum))

localSearch(cyclesAndSum)