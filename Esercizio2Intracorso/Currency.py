from StruttureDati.map.red_black_tree import RedBlackTreeMap as RB
from Esercizio1Intracorso.DoubleHashingHashMap import DoubleHashingHashMap as DHH
import copy


class Currency():

    def __init__(self, c):
        super().__init__()
        if c.isupper() and (len(c) == 3):
            self._Code = c
        else:
            raise KeyError('Key Format Error: keys must be of three upper capital letter' + repr(c))
        self._Denomination = RB()
        self._Changes = DHH()

    def getCode(self):
        return self._Code

    def AddDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        if (isinstance(value,float) or isinstance(value,int)) and value > 0.0:
            self._Denomination.__setitem2__(value,None)
        else:
            raise ValueError('Value must be numeric and positive. ' + repr(value))

    def DelDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        self._Denomination.__delitem__(value)

    def MinDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        k = self._Denomination.find_min()
        if value is None:
            if k is None:
                raise KeyError('Key Error: ' + repr(k))  # empty tree
            return k
        else:
            gt = self._Denomination.find_gt(value)
            if gt is None:
                raise KeyError('Key Error: ' + repr(value))  # does not exist such a key
            return gt

    def MaxDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        k = self._Denomination.find_max()
        if value is None:
            if k is None:
                raise KeyError('Key Error: ' + repr(k))  # empty tree
            return k
        else:
            lt = self._Denomination.find_lt(value)
            if lt is None:
                raise KeyError('Key Error: ' + repr(value))  # does not exist such a key
            return lt

    def nextDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        p = self._Denomination.find_position(value)
        if p.element()._key != value:
            raise KeyError('Key Error: ' + repr(value))  # the key "value" does not exist
        elif p == self._Denomination.last():
            return None  # does not exist a key that is grater than "value"
        p_true = self._Denomination.after(p)
        return (p_true.element()._key, p_true.element()._value)

    def prevDenomination(self,value):
        """Complexity -> O(log(n)) ; O(1) if tree consists only of the root node"""
        p = self._Denomination.find_position(value)
        if p.element()._key != value:
            raise KeyError('Key Error: ' + repr(value))  # the key "value" does not exist
        elif p == self._Denomination.first():
            return None  # does not exist a key that is less than "value"
        p_true = self._Denomination.before(p)
        return p_true.element()._key

    def hasDenominations(self):
        """Complexity = O(1)"""
        return self._Denomination.is_empty()

    def numDenominations(self):
        """Complexity = O(1)"""
        return self._Denomination.__len__()

    def clearDenominations(self):
        """Complexity = O(1)"""
        self._Denomination.clear()

    def iterDenominations(self, reverse):
        """Complexity -> O(n)"""
        if reverse:
            return self._Denomination.__reversed__()
        else:
            return self._Denomination.__iter__()

    def addChange(self, currencycode, change):
        """
            Best case = O(1) if tree consists only of the root node
            Average Case = O(1/(1-λ)) ; 0<λ≤0.5
            Worst Case = O(n)
        """
        check_float = isinstance(change, float)
        if check_float and change > 0.0:
            h = self._Changes._hash_function(currencycode)
            found,x = self._Changes._find_slot(h,currencycode,False)
            if found:
                raise KeyError('Currency Error: ' + repr(currencycode))     #key already exists
            else:
                if currencycode != self._Code:
                    self._Changes.__setitem__(currencycode,change)
                else:
                    raise KeyError('Currency Error: ' + repr(currencycode))     #can't insert a currency equals to _Code
        else:
            raise KeyError('Currency Error: ' + repr(change))  # change must be float

    def removeChange(self, currencycode):
        """
            Best case = O(1) if tree consists only of the root node
            Average Case = O(1/(1-λ)) ; 0<λ≤0.5
            Worst Case = O(n)
        """
        self._Changes.__delitem__(currencycode)

    def updateChange(self, currencycode, change):
        """
            Best case = O(1) if tree consists only of the root node
            Average Case = O(1/(1-λ)) ; 0<λ≤0.5
            Worst Case = O(n)
        """
        check_float = isinstance(change, float)
        if check_float:
            self._Changes.__setitem__(currencycode,change)
        else:
            raise KeyError('Currency Error: ' + repr(change))  # change must be float

    def copy(self):
        """Complexity = O(1)"""
        return copy.copy(self)

    def deepcopy(self):
        """Complexity = O(n)"""
        curr2 = Currency(self._Code)
        iteratore1 = self._Denomination.__iter__()
        for i in iteratore1:
            curr2.AddDenomination(i)
        iteratore2 = self._Changes.__iter__()
        for i in iteratore2:
            curr2.addChange(i, self._Changes.__getitem__(i))
        return curr2

    def toStringDenomination(self):
        iteratore = self._Denomination.__iter__()
        for i in iteratore:
            print("Key: ", i, ";    Value: ", self._Denomination.__getitem__(i))

    def toStringChanges(self):
        iteratore = self._Changes.__iter__()
        for i in iteratore:
            print("Key: ", i, ";    Value: ", self._Changes.__getitem__(i))

    def toString(self):
        print("CODE:", self._Code, "\t-\tDENOMINATION:", end=" ")
        iteratore1 = self._Denomination.__iter__()
        count = 1
        for i in iteratore1:
            if count != self.numDenominations():
                print("(Key: ", i, ", Value: ", self._Denomination.__getitem__(i), ")", sep='', end="; ")
            else:
                print("(Key: ", i, ", Value: ", self._Denomination.__getitem__(i), ")", sep='', end=" ")
            count += 1
        print("\t-\tCHANGES:", end=" ")
        iteratore2 = self._Changes.__iter__()
        count = 1
        for i in iteratore2:
            if count != self.numDenominations():
                print("(Key: ", i, ", Value: ", self._Changes.__getitem__(i), ")", sep='', end="; ")
            else:
                print("(Key: ", i, ", Value: ", self._Changes.__getitem__(i), ")", sep='', end=" ")
            count += 1
        print("\n")