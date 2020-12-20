from Esercizio2Intracorso.Currency import Currency
import decimal

# r = amount
# curr.numDenominations()
def dynamic(curr, r):
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

    return a

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
curr.AddDenomination(0.02)
curr.AddDenomination(0.03)
curr.AddDenomination(0.05)
curr.AddDenomination(0.1)

r = 0.15

a = dynamic(curr, r)
print("  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5]\n")
appoggio = [2,3,5,1]
j=0
for i in a:
    print(appoggio[j], i)
    j+=1
