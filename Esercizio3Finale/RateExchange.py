from StruttureDati.graphs.graph import Graph
from Esercizio2Intracorso.Currency import Currency
from math import exp


def DFSNegCycle(g, v, discovered, sum):
    """
    :param g: graph
    :param v: starting vertex who changes at each recursion
    :param discovered: list of vertex that make up a cycle
    :param sum: sum of all edges involved in the path constituting the cycle
    :return: a tuple is composed of 3 values: a boolean useful to know if we have found a cycle or not, a list of
             vertices that make up a cycle and the sum of all the arcs involved in the path constituting the cycle
    """

    for edge in g.incident_edges(v):
        vertex = edge.opposite(v)
        sum += edge.element()
        if vertex == discovered[0] and sum < 0 and len(discovered) > 1:
            discovered.append(vertex)
            return True, discovered, sum
        elif vertex not in discovered:
            discovered.append(vertex)
            check, cycle, sum = DFSNegCycle(g, vertex, discovered, sum)
            if check == True:
                return True, cycle, sum
            discovered.remove(vertex)
        sum -= edge.element()
    return False, discovered, sum

def arbitrageOpportunity(C, s):
    """
    :param C: set of Currency objects (we have supposed it is a list)
    :param s: a currency object
    :return: tuple whose first element is a list of a cycle, and whose second element is the rate exchange obtained
             through cycle
    """

    for curr in C:
        if not isinstance(curr, Currency):
            return "The set 'C' must contain only currency objects."

    if not isinstance(s, Currency):
        return "'s' must be a currency object."

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

    cycle = [v]
    tupla = DFSNegCycle(G, v, cycle, 0)
    check = tupla[0]
    if check:
        negCycle = tupla[1]
        sum = tupla[2]
        return negCycle, exp(-sum)
    return check
