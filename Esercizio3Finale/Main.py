from Esercizio2Intracorso.Currency import Currency
from Esercizio3Finale import RateExchange as re


# ----------CURRENCY INITIALIZATION-----------#
currUSD = Currency("USD")
currEUR = Currency("EUR")
currGBP = Currency("GBP")

#--------------CHANGES--------------#
currUSD.addChange("EUR", 0.32)
currEUR.addChange("GBP", 0.09)
currGBP.addChange("USD", 0.43)
currEUR.addChange("USD", -0.31)
currGBP.addChange("EUR", -0.87)
currUSD.addChange("GBP", -0.05)

C = [currUSD, currEUR, currGBP]   # we have supposed that the set of element containing Currency objects is a list
s = currUSD

#-------------TESTING ARBITRAGE OPPORTUNITY-----------#
cycleAndRate = re.arbitrageOpportunity(C, s)
if isinstance(cycleAndRate, tuple):
    print("Cycle that witness arbitrage opportunity:", end=" ")
    for currency in cycleAndRate[0]:
        print(currency.element()._Code, end=" ")
    print(".   By exchanging 1 " + s._Code + ", one receives " + str(cycleAndRate[1]) + " " + s._Code)
else:
    print(cycleAndRate)