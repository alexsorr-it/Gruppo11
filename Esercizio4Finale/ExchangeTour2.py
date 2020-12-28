from StruttureDati.graphs.graph import Graph
from Esercizio2Intracorso.Currency import Currency


def dfs(graph, start, end):
    """
    :param graph:
    :param start: start vertex
    :param end: end vertex
    :return: all cycles involved in the graph
    """
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
    """

    :param G: graph
    :return: all cycles that cover all vertex of the graph
    """

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
        #adding only cycles which include all vertices of the graph
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


