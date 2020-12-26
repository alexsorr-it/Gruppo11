from StruttureDati.graphs.graph import Graph
from math import exp


# This algorithm may returns a cycle in which is not involved the currency passed as parameter to the function
# "arbitrageOpportunity". Nevertheless, it will returns the first negative cycle found (if exists one), else False.

def isNegCycleBellmanFord(g, v):
    """
    :param g: graph
    :param v: vertex of which we want to find if there is a negative cycle
    :return: tuple whose first element is a list of a cycle, and whose second element is the rate exchange obtained
             through cycle
    """
    dist = {}     # dictionary containing vertex as keys and labels associate to each vertex, as values
    parent = {}   # dictionary containing vertex both for keys and values; the key ones are vertex destination
                  # of an edge; the value ones are vertex source of the same edge

    # setting initial values to dictionary
    for vertex in g.vertices():
        if vertex == v:
            dist[vertex] = 0
        else:
            dist[vertex] = 1000000
        parent[vertex] = -1

    # Relax all edges |V| - 1 times
    for vertex in g.vertices():
        for edge in g.edges():
            source = edge.endpoints()[0]
            destination = edge.endpoints()[1]
            weight = edge.element()
            if (dist[source] != 1000000 and dist[source] + weight < dist[destination]):
                dist[destination] = dist[source] + weight
                parent[destination] = source

    # Check for negative-weight cycles.
    # The above step guarantees shortest distances if graph doesn't contain negative weight cycle.
    # If we get a shorter path, then there is a cycle.
    negCycle = -1
    for edge in g.edges():
        source = edge.endpoints()[0]
        destination = edge.endpoints()[1]
        weight = edge.element()
        if (dist[source] != 1000000 and dist[source] + weight < dist[destination]):
            negCycle = destination
            break

    # detecting the cycle found
    if negCycle != -1:
        for vertex in g.vertices():
            negCycle = parent[negCycle]
        cycle = []
        vertex = negCycle
        while True:
            cycle.append(vertex)
            if (negCycle == vertex and len(cycle) > 1):
                break
            vertex = parent[vertex]
        weightEdges = 0
        cycleFound = cycle[::-1]
        cycleWellFormatted = []
        for index in range(0, len(cycleFound)-1):
            v1 = cycleFound[index]
            v2 = cycleFound[index + 1]
            edge = g.get_edge(v1, v2)
            weightEdges = weightEdges + edge.element()
            cycleWellFormatted.append(cycleFound[index].element()._Code)
            if index == len(cycleFound) - 2:
                cycleWellFormatted.append(cycleFound[index + 1].element()._Code)
        rateExchange = exp(-weightEdges)
        return (cycleWellFormatted, rateExchange)
    return False

def arbitrageOpportunity(C, s):
    """
    :param C: set of Currency objects (we have supposed it is a list)
    :param s: a currency object
    :return: tuple whose first element is a list of a cycle, and whose second element is the rate exchange obtained
             through cycle
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

    return isNegCycleBellmanFord(G, v)   # search for all cycles in the graph constructed
