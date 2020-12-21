from Esercizio3Intracorso.due_otto_tree import abTree as abt, SortedTableMap
from Esercizio2Intracorso.Currency import Currency
from StruttureDati.priority_queue.heap_priority_queue import HeapPriorityQueue as HPQ

def checkSumProduct(sorted, r, curr):
    print('Controllo prima le somme e poi i prodotti')
    #conteggio per la somma, 'sum_curr' avrà valori da 0 a r
    count = 0
    #questa lista mi conterrà tutte le priority queue
    sortedPriorityQueue = SortedTableMap()
    #la sorted map mi serve per valutare di volta in volta i vari elementi (cioè le denominations)
    min = sorted.find_min()
    print('MIN ', min[0])

    it = sorted.__iter__()
    for i in it:
        pq = HPQ()
        while r > 0:
            moneta = curr._Denomination.find_le(r)
            print('MONETA ',moneta)
            if moneta is None:
                raise KeyError('No coins less or equals than val. Val remaining: ' + repr(r))
            count += 1
            pq.add(moneta[0], count)
            r -= moneta[0]
            v = "{0:.2f}".format(r)
            r = float(v)
            print('VAL ', r)
            #aggiungo quindi alla sorted che mi contiene tutte le priority queue un nuovo elemento
            #che avrà come chiave il numero di monete usate per cambiare la valuta e come valore
            #la priority queue quindi le monete effettive usate per cambiare la valuta
            sortedPriorityQueue.__setitem__(pq.min()[1], pq)

            #ovviamente devo eliminare dalla sorted di partenza l'elemento usato come minimo
            #cosi alla prossima iterazione il minimo sarà il prossimo elemento e farò la stessa
            #cosa per il secondo elemento, quidni in pratica valuto per ogni elemento della sorted
            #tutte le possibili combinazioni di cambi

            #sorted.__delitem__(min[0])

    #per vedere il risultato finale quindi mi stampo le due sorted
    it = sorted.__iter__()
    for i in it:
        print(sorted.__getitem__(i))

    it = sortedPriorityQueue.__iter__()
    for i in it:
        print(sortedPriorityQueue.__getitem__(i))







def checkProductSum(sorted, r):
    print('Controllo prima i prodotti e poi le somme')

def calculateDenominations(curr, r):
    #do something
    check_float = isinstance(r, float)
    if check_float and r > 0.0:
        v = "{0:.2f}".format(r)
        val = float(v)
        print('VAL', val)
        count = 0
        #itero le denominations e le salvo in una sorted map
        listaDenominations = SortedTableMap()
        it = curr.iterDenominations(False)
        for d in it:
            print('ADD DENOMINATION ', d)
            listaDenominations.__setitem__(d, d)

        #stampo gli elementi della sorted map
        it = listaDenominations.__iter__()
        for i in it:
            print(listaDenominations.__getitem__(i))

        #a questo punto in 'listaDenominations' ho tutte le denomination possibili dell'oggetto Currency

        checkSumProduct(listaDenominations, r, curr)
        #checkProductSum(listaDenominations, r, curr)



def init():
    curr = Currency("EUR")

    # -----------DENOMINATION-------------#
    curr.AddDenomination(0.05)
    curr.AddDenomination(0.1)
    curr.AddDenomination(0.2)
    curr.AddDenomination(0.5)
    curr.AddDenomination(1)
    curr.AddDenomination(2)
    curr.AddDenomination(5)
    curr.AddDenomination(10)
    curr.AddDenomination(20)
    curr.AddDenomination(50)
    curr.AddDenomination(100)
    curr.AddDenomination(200)
    curr.AddDenomination(500)

    # #---------ADD DENOMINATION PRINT--------#
    curr.toStringDenomination()
    print("\n\n")
    calculateDenominations(curr, 0.6)



if __name__ == '__main__':
    init()




