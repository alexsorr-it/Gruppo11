from Esercizio3Intracorso.due_otto_tree import abTree as abt, SortedTableMap
from Esercizio2Intracorso.Currency import Currency

# complessità algoritmo: O(n^2), raggiunta nel while che comincia a riga 42 e richiama una funzione che esegue un ciclo for.
# Nel caso peggiore, il while e il for scorrono tutta la SortedTableMap contenente come chiavi, le chiavi dei nodi e come valori,
# il numero di valori compresi tra c1 e c2 che ciascun nodo dell'albero possiede.

# La soluzione Greedy in questo caso è sempre ottimale perché mi consente di prendere il minor numero di nodi che coprono
# (k,c1,c2). Non potrebbe esistere una situazione in cui si potrebbe trarre vantaggio non scegliendo l'ottimo locale.
# Esempio per assurdo:
#     Nodo 1 -> 10 valori compresi tra c1 e c2
#     Nodo 2 -> 2 valori compresi tra c1 e c2
#     Nodo 3 -> 1 valore compreso tra c1 e c2
# Per k=1, Greedy trova la soluzione nel Nodo 3 e restituisce 1 come numero di nodi -> ottimo globale.
# Per k=2, Greedy trova la soluzione nel Nodo 2 e  restituisce 1 come numero di nodi -> ottimo globale.
# Per k>2 e k<11, Greedy trova la soluzione nel Nodo 1 e  restituisce 1 come numero di nodi -> ottimo globale.
# Per k=11, Greedy trova la soluzione nel Nodo 1 e nel Nodo 3 e  restituisce 2 come numero di nodi -> ottimo globale.
# Per k=12, Greedy trova la soluzione nel Nodo 1 e nel Nodo 2 e  restituisce 2 come numero di nodi -> ottimo globale.
# Per k=13, Greedy trova la soluzione nel Nodo 1, nel Nodo 2 e nel Nodo 3 e  restituisce 3 come numero di nodi -> ottimo globale.
# Per k>13, viene restituito None in quanto non esistono >13 compresi tra c1 e c2 nell'esempio considerato.

def cover(tree, k, c1, c2):
    if c1 > c2:
        return "c2 must be greater than c1"

    #il metodo greatSearch presi in input due valori, mi restituisce tutti i nodi appartenenti
    #all'albero compresi tra questi due estremi.
    listaSorted = tree.greatSearch(c1,c2)

    # adesso in listaSorted ho tutti gli elementi compresi tra c1 e c2 e anche eventuali altri elementi che appartenevano ai nodi
    # cui c1 e c2 facevano parte.
    # Elimino i valori non compresi tra c1 e c2.

    listaChiaviDaCancellare = []
    for i in listaSorted:
        if i < c1 or i > c2:
            listaChiaviDaCancellare.append(i)
    for count in listaChiaviDaCancellare:
        listaSorted.__delitem__(count)

    # Adesso in listSorted ho tutti gli elementi che ho interesse ad analizzare.
    # Creo una SortedTableMap che conterrà come chiavi le chiavi dell'albero e come valore un contatore.
    # Questo contatore indica quanti elementi quel nodo possiede che sono compresi tra c1 e c2,

    sortedCount = SortedTableMap()
    giaInseriti = []
    for i in listaSorted:
        #per ogni elemento ovviamente azzero il contatore
        count = 0
        for j in listaSorted:
            if j >= i:
                # listaSorted.__getitem__(i) restituisce la chiave del nodo, cioè il min della sorted (?)
                if listaSorted.__getitem__(i) == listaSorted.__getitem__(j) and j not in giaInseriti:  # identità sulle chiavi
                    count += 1
                    giaInseriti.append(j)
                    sortedCount.__setitem__(listaSorted.__getitem__(i), count)

    # Ora ho sortedCount che contiene le chiavi e il numero di valori compresi tra c1 e c2 che rientrano nel nodo in questione.
    # Faccio una scelta Greedy fino a quando non copro k elementi. Se k non lo raggiungo neppure con tutti gli elementi compresi
    # tra c1 e c2, restituisco None

    num_nodi = 0
    while k > 0:
        num_nodi += 1  # aggiorno il numero di nodi necessari
        max = getMax(sortedCount)
        k = k - max
        if k <= 0:
            return num_nodi
        elif sortedCount.__len__() == 0:
            return None


def getMax(sortedCount):
    max = 0
    chiaveMax = 0
    for i in sortedCount:
        if max <= sortedCount.__getitem__(i):
            max = sortedCount.__getitem__(i)
            chiaveMax = i
    sortedCount.__delitem__(chiaveMax)
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
