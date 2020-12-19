from Esercizio2Intracorso.Currency import Currency

# r = amount
# curr.numDenominations()
def dynamic(curr, r):
    # initializing matrix 'a'
    adjust = []
    #if isinstance(r,float):

    a = [[1] * (r+1) for _ in range(0, curr.numDenominations())]

    it = curr.iterDenominations(False)
    coins = []
    for k in it:
        coins.append(k*100)

    for i in range(0, curr.numDenominations()):
        for j in range(1, r+1):
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





# ----------CURRENCY INITIALIZATION-----------#
curr = Currency("EUR")

# ----------CURRENCY CONSTRUCTION OBJECT----------#
# curr.AddDenomination(0.05)
# curr.AddDenomination(0.1)
# curr.AddDenomination(0.2)
# curr.AddDenomination(0.5)
# curr.AddDenomination(1)
# curr.AddDenomination(2)
# curr.AddDenomination(5)
# curr.AddDenomination(10)
# curr.AddDenomination(20)
# curr.AddDenomination(50)
# curr.AddDenomination(100)
# curr.AddDenomination(200)
# curr.AddDenomination(500)
curr.AddDenomination(2)
curr.AddDenomination(3)
curr.AddDenomination(5)
curr.AddDenomination(10)

r = 15
a = dynamic(curr, r)
for i in a:
    print(i)
