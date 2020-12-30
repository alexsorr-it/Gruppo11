from Esercizio2Intracorso.Currency import Currency
from Esercizio2Finale import CurrencyDynamic as cd


# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
curr.AddDenomination(1)
curr.AddDenomination(2)
curr.AddDenomination(5)

r = 6

tupla = cd.differentWays(curr, r)
if isinstance(tupla, tuple):
    n = tupla[0]
    totalCombinations = tupla[1]

    print("\nNumber of possible combinations:", n)
    print("\n\nPossible combinations:")
    if isinstance(totalCombinations, list):
        for combination in totalCombinations:
            print(combination)
    else:
        print(totalCombinations)
else:
    print(tupla)