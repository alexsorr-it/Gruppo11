from Esercizio2Intracorso.Currency import Currency
from Esercizio2Finale import CurrencyDynamic as cd


# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
#curr.AddDenomination(1)
curr.AddDenomination(2)
curr.AddDenomination(3)
curr.AddDenomination(4)
curr.AddDenomination(5)
curr.AddDenomination(10)
#curr.AddDenomination(13)



r = 10

tupla = cd.differentWays(curr, r)
if isinstance(tupla, tuple):
    n = tupla[0]
    totalCombinations = tupla[1]

    print("Number of possible combinations:", n)
    print("\n\nPossible combinations:")
    for combination in totalCombinations:
        print(combination)
else:
    print(tupla)