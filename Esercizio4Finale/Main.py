from Esercizio4Finale.ExchangeTour import localSearch
from Esercizio2Intracorso.Currency import Currency


#------------MAIN-----------------------#
curr1 = Currency("EUR")
curr2 = Currency("USD")
curr3 = Currency("GBP")
curr4 = Currency("CNY")
curr5 = Currency("JPY")
curr6 = Currency("OZZ")
curr7 = Currency("LEE")
curr8 = Currency("LAS")
curr9 = Currency("AAA")
curr10 = Currency("GNE")
curr11 = Currency("TOP")
curr12 = Currency("LAA")
curr13 = Currency("ANA")
curr14 = Currency("IMI")
curr15 = Currency("AVE")
curr16 = Currency("TRE")
curr17 = Currency("ROO")
curr18 = Currency("OOO")

#--------INPUT TRACCIA------#
curr1.addChange("USD", 0.3)
curr1.addChange("GBP", 0.31)
curr2.addChange("GBP", 0.09)
curr3.addChange("CNY", 0.05)
curr1.addChange("CNY", 0.87)
curr2.addChange("JPY", 0.43)
curr5.addChange("CNY", 0.11)
curr6.addChange("USD", 0.23)
curr6.addChange("LEE", 0.63)
curr7.addChange("EUR", 0.50)
curr7.addChange("CNY", 0.61)
curr8.addChange("OZZ", 0.82)
curr8.addChange("AAA", 0.21)
curr9.addChange("JPY", 0.87)
curr9.addChange("GNE", 0.57)
curr10.addChange("JPY", 0.44)
curr10.addChange("ANA", 0.20)
curr10.addChange("TOP", 0.10)
curr11.addChange("ANA", 0.30)
curr11.addChange("JPY", 0.20)
curr11.addChange("CNY", 0.40)
curr11.addChange("LAA", 1.20)
curr12.addChange("CNY", 0.70)
curr12.addChange("IMI", 0.50)
curr14.addChange("CNY", 0.80)
curr14.addChange("OOO", 0.50)
curr14.addChange("ROO", 0.90)
curr18.addChange("ROO", 2.40)
curr17.addChange("AVE", 0.30)
curr17.addChange("TRE", 0.40)
curr16.addChange("AVE", 1.40)
curr15.addChange("LEE", 0.9)

#-------------TESTING ARBITRAGE OPPORTUNITY-----------#
C = [curr2, curr1, curr3, curr4, curr5, curr6,
     curr7, curr8, curr9, curr10, curr11, curr12,
     curr13, curr14, curr15, curr16, curr17, curr18]   # we have supposed that the set of element containing Currency objects is a list

cyclesAndSum = localSearch(C)
if isinstance(cyclesAndSum, tuple):
     print("Exchange tour:", cyclesAndSum[0], "\nRate:", cyclesAndSum[1])
else:
     print(cyclesAndSum)
