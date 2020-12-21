# Copyright 2013, Michael H. Goldwasser
#
# Developed for use with the book:
#
#    Data Structures and Algorithms in Python
#    Michael T. Goodrich, Roberto Tamassia, and Michael H. Goldwasser
#    John Wiley & Sons, 2013
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

ONE_TIME_EXCECUTION = 0

def DFS(g, u, discovered):
  """Perform DFS of the undiscovered portion of Graph g starting at Vertex u.

  discovered is a dictionary mapping each vertex to the edge that was used to
  discover it during the DFS. (u should be "discovered" prior to the call.)
  Newly discovered vertices will be added to the dictionary as a result.
  """
  for e in g.incident_edges(u):    # for every outgoing edge from u
    v = e.opposite(u)
    if v not in discovered:        # v is an unvisited vertex
      discovered[v] = e            # e is the tree edge that discovered v
      DFS(g, v, discovered)        # recursively explore from v


#metodo definito ad hoc per la risoluzione dell'esercizio 4
def DFS_exchangeTour(g, startVertex, u, discovered, exchangeTour, score, countVertex):
  """Perform DFS of the undiscovered portion of Graph g starting at Vertex u.

  discovered is a dictionary mapping each vertex to the edge that was used to
  discover it during the DFS. (u should be "discovered" prior to the call.)
  Newly discovered vertices will be added to the dictionary as a result.
  """
  discovered[u] = None

  #mi inserisco nella lista il primo elemento, questo codice lo faccio
  #solo alla prima esecuzione, quando il contatore che mi tiene traccia dei
  #vertici è posto a 0 (0 = primo vertice visitato)
  if countVertex == 0:
    exchangeTour.append(startVertex)

  for e in g.incident_edges(u):    # for every outgoing edge from u
    #function check edge with minimum weight
    v = e.opposite(u)

    # quindi il peso dell'arco che mi porta a quell'arco
    if v.element() == startVertex.element() and countVertex == g.vertex_count() - 1:
      score += e.element()
      print('GOAL ', score)
      print("LAST vertex choose " + v.element() + " opposite to " + u.element() + " iteration: " + str(countVertex))
      return score
    if countVertex == g.vertex_count() - 1:
      score += e.element()
      print('GOAL ', score)
      return score

    if v not in discovered:        # v is an unvisited vertex
      countVertex += 1
      #per chiudere il ciclo (tour) devo considerare anche il vertice di partenza
      discovered[v] = e            # e is the tree edge that discovered v
      exchangeTour.append(v)
      score += e.element()
      print('GOAL ', score)
      print("vertex choose " + v.element() + " opposite to " + u.element() + " iteration: " + str(countVertex))
      DFS_exchangeTour(g, startVertex, v, discovered, exchangeTour, score, countVertex)        # recursively explore from v


def construct_path(u, v, discovered):
  """
  Return a list of vertices comprising the directed path from u to v,
  or an empty list if v is not reachable from u.

  discovered is a dictionary resulting from a previous call to DFS started at u.
  """
  path = []                        # empty path by default
  if v in discovered:
    # we build list from v to u and then reverse it at the end
    path.append(v)
    walk = v
    while walk is not u:
      e = discovered[walk]         # find edge leading to walk
      parent = e.opposite(walk)
      path.append(parent)
      walk = parent
    path.reverse()                 # reorient path from u to v
  return path

def DFS_complete(g):
  """Perform DFS for entire graph and return forest as a dictionary.

  Result maps each vertex v to the edge that was used to discover it.
  (Vertices that are roots of a DFS tree are mapped to None.)
  """
  forest = {}
  for u in g.vertices():
    if u not in forest:
      forest[u] = None             # u will be the root of a tree
      DFS(g, u, forest)
  return forest
