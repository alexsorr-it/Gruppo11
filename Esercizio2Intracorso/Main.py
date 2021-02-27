from Esercizio2Intracorso.Currency import Currency



curr = Currency("EUR")

#-----------DENOMINATION-------------#
curr.AddDenomination(1)
curr.AddDenomination(3)
curr.AddDenomination(5)
curr.AddDenomination(7)
curr.AddDenomination(4)

#---------ADD DENOMINATION PRINT--------#
# curr.toStringDenomination()
# print("\n\n")

# #---------DELETE DENOMINATION-------#
# curr.toStringDenomination()
# curr.DelDenomination(3)
# curr.DelDenomination(4)
# print("\n\n")
# curr.toStringDenomination()
#
# a = None
# a = 7
# b = 3
# print("Chiave minima tra quelle più grandi di ", a, ": ", curr.MinDenomination(a))
# print("Chiave massima tra quelle più piccole di ", b, ": ", curr.MaxDenomination(b))
#
# c = 5
# print("next denomination of", c, ":", curr.nextDenomination(c))
# d = 5
# print("previous denomination of", d, ":", curr.prevDenomination(d))
#
# print("denominations is empty:", curr.hasDenominations())
# print("number of denominations:", curr.numDenominations())
#
# print("\nDenomination before clear:")
# curr.toStringDenomination()
# curr.clearDenominations()
# print("\nDenomination after clear:")
# curr.toStringDenomination()
#
# #--------ITER DENOMINATION----------#
# print("\nNormal iteration:")
# iteratore = curr.iterDenominations(False)
# for i in iteratore:
#     print("Key: ", i, ";    Value: ", curr._Denomination.__getitem__(i))
# print("\n\nReverse iteration:")
# iteratore = curr.iterDenominations(True)
# for i in iteratore:
#     print("Key: ", i, ";    Value: ", curr._Denomination.__getitem__(i))
#
# #--------------CHANGES--------------#
curr.addChange("DOL", -9)
curr.addChange("LOD", 3.0)
curr.addChange("OLD", 7.0)
# curr.toStringChanges()
#
# #--------REMOVE CHANGES----------#
# print("\n\n")
# curr.removeChange("LOD")
# print("\n\nAfter delete:")
# curr.toStringChanges()
#
# #--------CHECK UPDATE CHANGES----------#
# curr.updateChange("OLD", 12.0)
# print("\n\nAfter update:")
# curr.toStringChanges()
#
# #--------CHECK COPY AND DEEPCOPY DENOMINATION----------#
curr2 = curr.copy()
print("\nCURRENCY INIZIALE:")
curr.toString()
print("\n\nCOPY (WITH COPY MODIFICATIONS):")
curr2.AddDenomination(8)
curr2.addChange("LDO", 8.0)
curr2.toString()
print("\n\nCURRENCY POST COPY:")
curr.toString()
curr3 = curr.deepcopy()
print("\n\nDEEPCOPY (WITH COPY AND DEEPCOPY MODIFICATIONS):")
curr3.AddDenomination(9)
curr3.addChange("DLO", 9.0)
curr3.toString()
print("\n\nCURRENCY POST DEEPCOPY:")
curr.toString()
#
# #--------CHECK COLOUR NODE----------#
# generator = curr._Denomination.__iter__()
# for i in generator:
#     print("Key: ", i, ";    Value: ", curr._Denomination.__getitem__(i))
#     print(curr._Denomination._is_red(curr._Denomination.find_position(i)))