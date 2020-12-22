from Esercizio2Intracorso.Currency import Currency
import decimal

# r = amount
# curr.numDenominations()
def differentWays(curr, r):
    d = decimal.Decimal(str(r))
    var = d.as_tuple().exponent
    if var < -2:
        return "value with over two decimal points are not allowed"

    r = int(r * 100)

    # initializing matrix 'a'
    a = [[1] * (r+1) for _ in range(0, curr.numDenominations())]

    it = curr.iterDenominations(False)
    coins = []
    for k in it:
        d = decimal.Decimal(str(k))
        var = d.as_tuple().exponent
        if var < -2:
            return "value with over two decimal points are not allowed"
        coins.append(int(k * 100))

    for i in range(0, curr.numDenominations()):
        for j in range(1,r+1):
            if i == 0:
                if j % coins[0] == 0:
                    a[0][j] = 1
                else:
                    a[0][j] = 0
            elif coins[i] > j:
                a[i][j] = a[i-1][j]
            else:
                a[i][j] = a[i-1][j] + a[i][j-coins[i]]

    combinazioniTotali = []
    combinazione = []
    for i in range(curr.numDenominations() - 1, -1, -1):
        numCombinazioni = a[i][r-coins[i]]
        amount = r
        riga = i
        while numCombinazioni > 0:
            amount = amount - coins[riga]
            if amount >= 0:
                if [coins[riga], amount] not in combinazione:
                    combinazione.append([coins[riga], amount])
                    if amount == 0:
                        if combinazione not in combinazioniTotali:
                            combinazioniTotali.append(combinazione)
                            numCombinazioni -= numCombinazioni
                            amount = r
                            combinazione = []
                        else:
                            combinazione[combinazione.__len__() - 1].pop(combinazione[combinazione.__len__() - 1].__len__() - 1)
                            amount = amount + coins[riga]
                            riga = riga - 1
                else:
                    if amount == 0:
                        amount = amount + coins[riga]
                    riga = riga - 1
            else:
                amount = amount + coins[riga]
                riga = riga - 1

    # [ [coins1, amount1], [coins2, amount2], ... ]  -> combinazione
    # [  [[coins1, amount1], [coins2, amount2]], [[coins1, amount1], [coins2, amount2]], ...  ] -> combinazioniTotali
    grandeStringa = ""
    cEsterno = 0
    for i in combinazioniTotali:
        stringa = ""
        c = 0
        for j in i:
            coin = j[0]
            if c == 0:
                stringa = "(" + str(coin)
                c += 1
            elif c == i.__len__() - 1:
                stringa = stringa + ", " + str(coin) + ")"
            else:
                stringa = stringa + ", " + str(coin)
        if cEsterno == 0:
            grandeStringa = "combinazioni possibili: (" + stringa
        elif cEsterno == combinazioniTotali.__len__() - 1:
            grandeStringa = grandeStringa + ", " + stringa + ")"
        else:
            grandeStringa = grandeStringa + ", " + stringa

    return (a, grandeStringa)





# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
curr.AddDenomination(0.02)
curr.AddDenomination(0.03)
curr.AddDenomination(0.05)
curr.AddDenomination(0.1)

r = 0.15

tupla = differentWays(curr, r)
a = tupla[0]
gs = tupla[1]
print("  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5]\n")
appoggio = [2,3,5,1]
j=0
for i in a:
    print(appoggio[j], i)
    j+=1

print("\n" + gs)
