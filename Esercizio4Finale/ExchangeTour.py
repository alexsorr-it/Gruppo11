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
score = 0

DFS_exchangeTour(grafo, v1, v1, listCurrency, exchangeTour, score, 0)

print('EXCHANGE TOUR')
for curr in exchangeTour:
    print(curr)

isValid = True
for i in range(0, len(exchangeTour) - 1):   # i va da 0 a 4
    if not grafo.get_edge(exchangeTour[i], exchangeTour[i+1]):
        print('exchange tour is not valid')
        isValid = False

if(isValid):
    print('exchange tour is valid with score ', score)

#quando mettiamo come vertice iniziale v4 ci troviamo nel secondo caso di errore del problema
