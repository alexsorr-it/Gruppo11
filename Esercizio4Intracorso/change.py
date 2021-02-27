from Esercizio2Intracorso.Currency import Currency
from StruttureDati.priority_queue.heap_priority_queue import HeapPriorityQueue as HPQ

def change(value, curr):
    check_float = isinstance(value, float)
    check_curr = isinstance(curr, Currency)
    if not check_curr:
        raise ValueError('curr must be a Currency object. ' + repr(curr))
    if check_float and value > 0.0:
        v = "{0:.2f}".format(value)
        val = float(v)
        count = 0
        pri = HPQ()
        while val > 0:
            moneta = curr._Denomination.find_le(val)
            if moneta is None:
                raise KeyError('No coins less or equals than val. Val remaining: ' + repr(val))
            count += 1
            pri.add(moneta[0], count)
            val -= moneta[0]
            v = "{0:.2f}".format(val)
            val = float(v)
        return (pri.min()[1], pri)
    else:
        raise ValueError('Value must be float. ' + repr(value))

def stampa(tupla, curr):
    priorityQueue = tupla[1]
    lista = []
    for i in range(0, priorityQueue.__len__()):
        lista.append(priorityQueue.remove_min()[0])
    print("Number of coins used:", tupla[0], "\tType of coins used:", lista[::-1], "\t\tCurrency used:", curr._Code)
    #--------REINSERIMENTO--------#
    for i in range(0,len(lista)):
        priorityQueue.add(lista[i],None)



#----------CURRENCY INITIALIZATION-----------#
curr1 = Currency("EUR")
curr2 = Currency("USD")

#----------CURRENCY CONSTRUCTION OBJECT----------#
curr1.AddDenomination(0.05)
curr1.AddDenomination(0.1)
curr1.AddDenomination(0.2)
curr1.AddDenomination(0.5)
curr1.AddDenomination(1)
curr1.AddDenomination(2)
curr1.AddDenomination(5)
curr1.AddDenomination(10)
curr1.AddDenomination(20)
curr1.AddDenomination(50)
curr1.AddDenomination(100)
curr1.AddDenomination(200)
curr1.AddDenomination(500)
curr1.addChange("USD", 1.2)

curr2.AddDenomination(0.01)
curr2.AddDenomination(0.05)
curr2.AddDenomination(0.1)
curr2.AddDenomination(0.25)
curr2.AddDenomination(0.5)
curr2.AddDenomination(1)
curr2.AddDenomination(2)
curr2.AddDenomination(5)
curr2.AddDenomination(10)
curr2.AddDenomination(20)
curr2.AddDenomination(50)
curr2.AddDenomination(100)
curr2.addChange("EUR", 0.85)

#-----------PRINT RESULTS-------------#
tupla1 = change(12.85, curr1)
stampa(tupla1, curr1)
tupla2 = change(12.85, curr2)
stampa(tupla2, curr2)