from Esercizio2Intracorso.Currency import Currency
from Esercizio2Finale import CurrencyDynamic as cd


# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
curr.AddDenomination(2)
curr.AddDenomination(3)
curr.AddDenomination(5)
curr.AddDenomination(10)

r = 15

tupla = cd.differentWays(curr, r)
if isinstance(tupla, tuple):
    a = tupla[0]
    gs = tupla[1]

    print("Number of possible combinations:", a)
    print("\n\nPossible combinations:")
    for i in gs:
        print(i)
else:
    print(tupla)