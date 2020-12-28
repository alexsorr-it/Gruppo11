from StruttureDati.graphs.graph import Graph
from Esercizio2Intracorso.Currency import Currency


def dfs(graph, start, end):
    """
    :param graph: graph
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

def adaptingGraph(G):
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
        # adding only cycles which include all vertices of the graph
        if len(cycle) - 1 == len(G.vertices()):
            cycles.append(cycle)
    return cycles

def constructingGraph(C):
    """
    :param C: set
    :return:
    """
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

    cycles = adaptingGraph(G)
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

def localSearch(C):
    """
    Local search Algorithm
    - We mantain the current solution S
    - We mantain the current best solution S*
    - We choose a solution S' in N(S)
    - We set S' as the new current solution
    - If c(S') < c(S*), we set S' as the current best solution
    - Repeat

    :param C: set of Currency objects (supposed a list)
    :return: tuple containing as first element the list of the cycle found and as second element the relative
             rate exchange
    """

    for curr in C:
        if not isinstance(curr, Currency):
            return "The set 'C' must contain only currency objects."
        it = curr._Changes.__iter__()
        for i in it:
            if curr._Changes.__getitem__(i) <= 0:
                return "We have assumed that if the rate exchange r(c, c’) exists, then also r(c’, c) exists and" \
                       " r(c, c’) = r(c’, c) > 0."

    cyclesAndSum = constructingGraph(C)

    if len(cyclesAndSum) == 0:
        return "There is no valid exchange tour."

    #Neighbour-hood relation (two solution differ from each other by the start vertex choosen for the DFS algorithm)
    score = cyclesAndSum[0][1]
    currentBestSolution = cyclesAndSum[0][0]
    index = 0
    while index < len(cyclesAndSum):
        current_score = cyclesAndSum[index][1]
        if current_score < score:
            score = current_score
            currentBestSolution = cyclesAndSum[index][0]
        index += 1

    return currentBestSolution, score
