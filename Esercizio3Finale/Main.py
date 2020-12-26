from Esercizio2Intracorso.Currency import Currency
from Esercizio3Finale import RateExchangeDFS as redfs

# ----------CURRENCY INITIALIZATION-----------#
currUSD = Currency("USD")
currEUR = Currency("EUR")
currGBP = Currency("GBP")

#--------------CHANGES--------------#
currUSD.addChange("EUR", -0.005)
currEUR.addChange("GBP", 0.004)
currGBP.addChange("USD", 0.005)
currEUR.addChange("USD", 0.004)
currGBP.addChange("EUR", 0.005)
currUSD.addChange("GBP", 0.004)

C = [currUSD, currEUR, currGBP]   # we have supposed that the set of element containing Currency objects is a list
s = currGBP

#-------------TESTING ARBITRAGE OPPORTUNITY-----------#
cycleAndRate = redfs.arbitrageOpportunity(C, s)
if(isinstance(cycleAndRate, tuple)):
    cycle = cycleAndRate[0]
    rateExchange = cycleAndRate[1]
    print("Cycle found:", cycle, "\nBy exchanging 1", cycle[0], "one receives", rateExchange, cycle[0])
else:
    print(cycleAndRate)