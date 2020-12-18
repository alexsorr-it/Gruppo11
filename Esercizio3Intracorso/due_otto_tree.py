from collections.abc import MutableMapping


class MapBase(MutableMapping):
    """Our own abstract base class that includes a nonpublic _Item class."""

    # ------------------------------- nested _Item class -------------------------------
    class _Item:
        """Lightweight composite to store key-value pairs as map items."""
        __slots__ = '_key', '_value', '_figlio'

        def __init__(self, k, v):
            self._key = k
            self._value = v
            self._figlio = SortedTableMap()

        def __eq__(self, other):
            return self._key == other._key  # compare items based on their keys

        def __ne__(self, other):
            return not (self == other)  # opposite of __eq__

        def __lt__(self, other):
            return self._key < other._key  # compare items based on their keys


class SortedTableMap(MapBase):
    """Map implementation using a sorted table."""

    # ----------------------------- nonpublic behaviors -----------------------------
    def _find_index(self, k, low, high):
        """Return index of the leftmost item with key greater than or equal to k.

        Return high + 1 if no such item qualifies.

        That is, j will be returned such that:
           all items of slice table[low:j] have key < k
           all items of slice table[j:high+1] have key >= k
        """
        # devi applicare il metodo inorder per cercare nel modo illustrato a pagina 331
        if high < low:
            return high + 1  # no element qualifies
        else:
            mid = (low + high) // 2
            if k == self._table[mid]._key:
                return mid  # found exact match
            elif k < self._table[mid]._key:
                return self._find_index(k, low, mid - 1)  # Note: may return mid
            else:
                return self._find_index(k, mid + 1, high)  # answer is right of mid

    # ----------------------------- public behaviors -----------------------------
    def __init__(self):
        """Create an empty map."""
        self._table = []

    def __len__(self):
        """Return number of items in the map."""
        return len(self._table)

    def __getitem__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            # raise KeyError('Key Error: ' + repr(k))
            return None
        return self._table[j]._value

    def __setitem__(self, k, v):
        """Assign value v to key k, overwriting existing value if present."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j < len(self._table) and self._table[j]._key == k:
            self._table[j]._value = v  # reassign value
        else:
            self._table.insert(j, self._Item(k, v))  # adds new item

    def __getson__(self, k):
        """Return value associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        return self._table[j]._figlio

    def __setson__(self, k, sm2):
        j = self._find_index(k, 0, len(self._table) - 1)
        iteratore = sm2.__iter__()
        for i in iteratore:
            self._table[j]._figlio.__setitem__(i, sm2.__getitem__(i))

    def __delitem__(self, k):
        """Remove item associated with key k (raise KeyError if not found)."""
        j = self._find_index(k, 0, len(self._table) - 1)
        if j == len(self._table) or self._table[j]._key != k:
            raise KeyError('Key Error: ' + repr(k))
        self._table.pop(j)  # delete item

    def __iter__(self):
        """Generate keys of the map ordered from minimum to maximum."""
        for item in self._table:
            yield item._key

    def __reversed__(self):
        """Generate keys of the map ordered from maximum to minimum."""
        for item in reversed(self._table):
            yield item._key

    def find_min(self):
        """Return (key,value) pair with minimum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[0]._key, self._table[0]._value)
        else:
            return None

    def find_max(self):
        """Return (key,value) pair with maximum key (or None if empty)."""
        if len(self._table) > 0:
            return (self._table[-1]._key, self._table[-1]._value)
        else:
            return None

    def find_le(self, k):
        """Return (key,value) pair with greatest key less than or equal to k.

        Return None if there does not exist such a key.
        """
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j < len(self._table) and self._table[j]._key == k:
            return (self._table[j]._key, self._table[j]._value)  # exact match
        elif j > 0:
            return (self._table[j - 1]._key, self._table[j - 1]._value)  # Note use of j-1
        else:
            return None

    def find_ge(self, k):
        """Return (key,value) pair with least key greater than or equal to k.

        Return None if there does not exist such a key.
        """
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_lt(self, k):
        """Return (key,value) pair with greatest key strictly less than k.

        Return None if there does not exist such a key.
        """
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j > 0:
            return (self._table[j - 1]._key, self._table[j - 1]._value)  # Note use of j-1
        else:
            return None

    def find_gt(self, k):
        """Return (key,value) pair with least key strictly greater than k.

        Return None if there does not exist such a key.
        """
        j = self._find_index(k, 0, len(self._table) - 1)  # j's key >= k
        if j < len(self._table) and self._table[j]._key == k:
            j += 1  # advanced past match
        if j < len(self._table):
            return (self._table[j]._key, self._table[j]._value)
        else:
            return None

    def find_range(self, start, stop):
        """Iterate all (key,value) pairs such that start <= key < stop.

        If start is None, iteration begins with minimum key of map.
        If stop is None, iteration continues through the maximum key of map.
        """
        if start is None:
            j = 0
        else:
            j = self._find_index(start, 0, len(self._table) - 1)  # find first result
        while j < len(self._table) and (stop is None or self._table[j]._key < stop):
            yield (self._table[j]._key, self._table[j]._value)
            j += 1



from Esercizio3Intracorso.my_binary_tree_search import TreeMap as TM



class abTree():

    def __init__(self):
        self._Mappa = SortedTableMap()
        self._Albero = TM()
        self._dictionary = {}

    def reset_key(self, p, k):
        mappa = SortedTableMap()
        iteratore2 = p.value().__iter__()
        for i in iteratore2:
            mappa.__setitem__(i, p.value().__getitem__(i))
            mappa.__setson__(i, p.value().__getson__(i))
        self._Albero.__delitem__(p.key())  # cancello la entry con chiave minima
        self._Albero.__setitem2__(k, mappa)  # reinserisco la entry con nuova chiave minima

    def addElement(self, k, v):
        if self._Albero.is_empty():
            self._Mappa.__setitem__(k, v)
            self._Albero.__setitem__(k, self._Mappa)
            return
        p = self._Albero.find_position(k)
        if (k > p.value().find_max()[0] and not self._Albero.is_leaf(p) or (k < p.key() and self._Albero.parent(p).key() < p.key() and self._Albero.is_leaf(p))):
            p = self._Albero.parent(p)
        self._dictionary.__setitem__("position", p)
        self.ins2(k, v, p, p.value())

    def ins2(self, k, v, p, sorted):
        tupla = sorted.find_ge(k)
        if tupla is not None:
            k_pot = tupla[0]
            if k_pot == k:
                sorted.__setitem__(k, v)
            elif k_pot > k:
                if sorted.__getson__(k_pot).__len__() > 0:
                    self._dictionary.__setitem__(k_pot, sorted)
                    self.ins2(k, v, p, sorted.__getson__(k_pot))
                else:
                    sorted.__setitem__(k, v)
                    if p.value() == sorted:
                        self.split(p, None)  # split nodo
                    else:
                        self.split(None, sorted)  # split riferimento
                        self._dictionary = {}
        else:
            sorted.__setitem__(k, v)
            if p.value() == sorted:
                self.split(p, None)  # split nodo
            else:
                self.split(None, sorted)  # split riferimento
                self._dictionary = {}

    def split(self, p, map):
        if p is None and map is not None:
            mappa = map
        elif map is None and p is not None:
            mappa = p.value()
        else:
            return None
        if mappa.__len__() >= 8:
            middle = (mappa.__len__() - 1) // 2
            k_mid = mappa._table[middle]._key
            sm1 = SortedTableMap()
            sm2 = SortedTableMap()
            sm3 = SortedTableMap()
            iteratore = mappa.__iter__()
            for i in iteratore:
                if i < k_mid:
                    sm2.__setitem__(i, mappa.__getitem__(i))
                elif i > k_mid:
                    sm3.__setitem__(i, mappa.__getitem__(i))
            sm1.__setitem__(k_mid, mappa.__getitem__(k_mid))
            self.son_recursive(sm1, mappa)
            self.son_recursive(sm2, mappa)
            self.son_recursive(sm3, mappa)
            if map is None and p is not None:
                if self._Albero.is_root(p):
                    self._Albero.__setitem2__(sm1.find_min()[0], sm1)
                    self._Albero.__setitem2__(sm2.find_min()[0], sm2)
                    self._Albero.__setitem2__(sm3.find_min()[0], sm3)
                    return
                self._Albero.parent(p).value().__setitem__(k_mid, sm1.__getitem__(k_mid))
                if p.key() > self._Albero.parent(p).key():
                    self._Albero.parent(p).value().__setson__(k_mid, sm2)
                    self.son_recursive(self._Albero.parent(p).value().__getson__(k_mid), mappa)
                    self._Albero.__delitem__(p.key())
                    self._Albero.__setitem2__(sm3.find_min()[0], sm3)
                    p = self._Albero.find_position(sm3.find_min()[0])
                elif p.key() < self._Albero.parent(p).key():
                    self._Albero.parent(p).value().__setson__(self._Albero.parent(p).key(), sm3)
                    self.son_recursive(self._Albero.parent(p).value().__getson__(self._Albero.parent(p).key()), mappa)
                    self._Albero.parent(p).value().__setson__(k_mid, mappa.__getson__(k_mid))
                    self.son_recursive(self._Albero.parent(p).value().__getson__(k_mid), mappa)
                    self._Albero.__delitem__(p.key())
                    self._Albero.__setitem2__(sm2.find_min()[0], sm2)
                    p = self._Albero.find_position(sm2.find_min()[0])
                    self.reset_key(self._Albero.parent(p), k_mid)
                    p = self._Albero.find_position(sm2.find_min()[0])
                if (self._Albero.parent(p).value().__len__() >= 8):
                    self.split(self._Albero.parent(p), None)
            elif map is not None and p is None:
                tup = self._dictionary.popitem()
                tup_k, tup_v = tup[0], tup[1]
                tup_v.__setitem__(k_mid, sm1.__getitem__(k_mid))
                tup_v.__setson__(k_mid, sm2)
                map.clear()
                it = sm3.__iter__()
                for i in it:
                    map.__setitem__(i, sm3.__getitem__(i))
                p = self._dictionary.__getitem__("position")
                if p.value() == tup_v:
                    if k_mid < p.key():
                        self.reset_key(p, k_mid)
                        p = self._Albero.find_position(k_mid)
                    self.split(p, None)
                else:
                    self.split(None, self._dictionary.popitem()[1])

    def son_recursive(self, sm, mappa):
        it = mappa.__iter__()
        for i in it:
            if mappa.__getson__(i).__len__() > 0 and sm.__getitem__(i) is not None:
                sm.__setson__(i, mappa.__getson__(i))
                self.son_recursive(mappa.__getson__(i), mappa.__getson__(i))

    def search(self, k):
        if self._Albero.is_empty():
            return None
        p = self._Albero.find_position(k)
        if (k > p.value().find_max()[0] and not self._Albero.is_leaf(p) or (k < p.key() and self._Albero.parent(p).key() < p.key())):
            p = self._Albero.parent(p)
        return self.search2(k, p.value())

    def search2(self, k, sorted):
        tupla = sorted.find_ge(k)
        if tupla is not None:
            k_pot, v_pot = tupla[0], tupla[1]
            if k_pot == k:
                return v_pot
            elif k_pot > k:
                if sorted.__getson__(k_pot).__len__() > 0:
                    return self.search2(k, sorted.__getson__(k_pot))
                else:
                    return None
        else:
            return None

    def searchSorted(self, k):
        if self._Albero.is_empty():
            return None
        p = self._Albero.find_position(k)
        if (k > p.value().find_max()[0] and not self._Albero.is_leaf(p) or (k < p.key() and self._Albero.parent(p).key() < p.key())):
            p = self._Albero.parent(p)
        return self.searchSorted2(k, p.value())

    def searchSorted2(self, k, sorted):
        tupla = sorted.find_ge(k)
        if tupla is not None:
            k_pot, v_pot = tupla[0], tupla[1]
            if k_pot == k:
                return sorted
            elif k_pot > k:
                if sorted.__getson__(k_pot).__len__() > 0:
                    return self.search2(k, sorted.__getson__(k_pot))
                else:
                    return None
        else:
            return None

    def delete(self, k):
        if self._Albero.is_empty():
            return None
        p = self._Albero.find_position(k)
        if (k > p.value().find_max()[0] and not self._Albero.is_leaf(p) or (k < p.key() and self._Albero.parent(p).key() < p.key())):
            p = self._Albero.parent(p)
        self.del2(k, p, p.value())

    def del2(self, k, p, sorted):
        tupla = sorted.find_ge(k)
        if tupla is not None:
            k_pot, v_pot = tupla[0], tupla[1]
            if k_pot == k:
                if self._Albero.is_root(p) and self._Albero.num_children(p) == 0:
                    sorted.__delitem__(k)
                    if p.value().__len__() >= 1 and self._Albero.is_leaf(p) and k == p.key():
                        self.reset_key(p, sorted.find_min()[0])
                    elif sorted.__len__() == 0:
                        self._Albero.__delitem__(k)
                    return
                if self._Albero.is_root(p) and self._Albero.left(p).value().__len__() == 1 and self._Albero.right(p).value().__len__() == 1:
                    sx = self._Albero.left(p).value().find_min()
                    dx = self._Albero.right(p).value().find_min()
                    p.value().clear()
                    p.value().__setitem__(sx[0], sx[1])
                    p.value().__setitem__(dx[0], dx[1])
                    self._Albero.__delitem__(sx[0])
                    self._Albero.__delitem__(dx[0])
                    self.reset_key(p, sx[0])
                    return
                if (sorted.__getson__(k).__len__() == 0 and sorted.__len__() > 1) or (p.value().__len__() > 1 and self._Albero.is_leaf(p)):
                    if k == p.value().find_min()[0] and not self._Albero.is_leaf(p):
                        if self._Albero.left(p).value().__len__() > 1 and p.value.__getson__(k).__len__() == 0:
                            max = self._Albero.left(p).value().find_max()
                            p.value().__setitem__(max[0], max[1])
                            self._Albero.left(p).value().__delitem__(max[0])
                            p.value().__delitem__(k)
                            self.reset_key(p, max[0])
                            return
                        elif p.value().__getson__(k).__len__() > 1:
                            bigger = p.value().__getson__(k).find_max()
                            p.value().__setitem__(bigger[0], bigger[1])
                            p.value().__getson__(k).__delitem__(bigger[0])
                            sons = p.value().__getson__(k)
                            p.value().__setson__(bigger[0], sons)
                            p.value().__delitem__(k)
                            self.reset_key(p, bigger[0])
                            return
                        elif p.value().__getson__(k).__len__() == 1 and self._Albero.left(p).value().__len__() > 1:
                            x = self._Albero.left(p).value().find_max()
                            p.value().__setitem__(x[0], x[1])
                            sons = p.value().__getson__(k)
                            p.value().__setson__(x[0], sons)
                            p.value().__delitem__(k)
                            self._Albero.left(p).value().__delitem__(x[0])
                            self.reset_key(p, x[0])
                            return
                        elif p.value().__getson__(k).__len__() == 1 and self._Albero.left(p).value().__len__() == 1:
                            son = p.value().__getson__(k).find_min()
                            self._Albero.left(p).value().__setitem__(son[0], son[1])
                            p.value().__delitem__(k)
                            self.reset_key(p, p.value().find_gt(k)[0])
                            return
                if (sorted.__getson__(k).__len__() == 0 and sorted.__len__() == 1) or (p.value().__len__() == 1 and self._Albero.is_leaf(p)):
                    if p.value().__len__() == 1 and self._Albero.is_leaf(p):
                        if p.key() > self._Albero.parent(p).key():
                            padre = self._Albero.parent(p)
                            max = padre.value().find_max()
                            if self._Albero.is_root(padre) and padre.value().__len__() == 1:
                                son_nodo = self._Albero.left(padre)
                                son = son_nodo.value()
                            else:
                                son = padre.value().__getson__(max[0])
                            if son.__len__() > 1:
                                max_son = son.find_max()
                                padre.value().__setitem__(max_son[0], max_son[1])
                                if not (self._Albero.is_root(padre) and padre.value().__len__() == 2):
                                    figli = padre.value().__getson__(max[0])
                                    padre.value().__setson__(max_son[0], figli)
                                    padre.value().__getson__(max_son[0]).__delitem__(max_son[0])
                                    padre.value().__getson__(max[0]).clear()
                                else:
                                    son.__delitem__(max_son[0])
                                if padre.key() > max_son[0]:
                                    self.reset_key(padre, max_son[0])
                                p.value().clear()
                                p.value().__setitem__(max[0], max[1])
                                self.reset_key(p, max[0])
                                self._Albero.root().value().__delitem__(max[0])
                            elif padre.value().__len__() > 1:
                                bigger = padre.value().find_max()
                                son_bigger = padre.value().__getson__(bigger[0]).find_min()
                                p.value().__setitem__(bigger[0], bigger[1])
                                p.value().__setitem__(son_bigger[0], son_bigger[1])
                                p.value().__delitem__(p.key())
                                self.reset_key(p, son_bigger[0])
                                padre.value().__delitem__(bigger[0])
                            elif son.__len__() == 1 and self._Albero.is_root(padre):
                                padre.value().__setitem__(son.find_min()[0], son.find_min()[1])
                                self.reset_key(padre, son.find_min()[0])
                                self._Albero.__delitem__(p.key())
                        elif p.key() < self._Albero.parent(p).key():
                            padre = self._Albero.parent(p)
                            min = padre.value().find_min()
                            if padre.value().__getson__(min[0]).__len__() > 0:
                                son = padre.value().__getson__(min[0])
                                sm = SortedTableMap()
                                sm.__setitem__(son.find_min()[0], son.find_min()[1])
                                self.son_recursive(sm, son)
                                c = 0
                                while sm.__getson__(sm.find_min()[0]).__len__() > 0:
                                    c += 1
                                    sm = sm.__getson__(sm.find_min()[0])
                                if c > 0:
                                    son.clear()
                                    it = sm.__iter__()
                                    for i in it:
                                        son.__setitem__(i, sm.__getitem__(i))
                            elif padre.value().__len__() == 1:
                                son = self._Albero.right(padre).value()
                            else:
                                son = padre.value().__getson__(padre.value().find_gt(min[0])[0])
                                sm = SortedTableMap()
                                sm.__setitem__(son.find_min()[0], son.find_min()[1])
                                self.son_recursive(sm, son)
                                c = 0
                                while sm.__getson__(sm.find_min()[0]).__len__() > 0:
                                    c += 1
                                    sm = sm.__getson__(sm.find_min()[0])
                                if c > 0:
                                    son.clear()
                                    it = sm.__iter__()
                                    for i in it:
                                        son.__setitem__(i, sm.__getitem__(i))
                            if son.__len__() > 1:
                                min_son = son.find_min()
                                padre.value().__setitem__(min_son[0], min_son[1])
                                son.__delitem__(min_son[0])
                                min_padre = padre.value().find_min()
                                nodo_sinistro = self._Albero.left(padre)
                                padre.value().__delitem__(padre.key())
                                if padre.value().__len__() == 1:
                                    self.reset_key(self._Albero.right(padre), son.find_min()[0])
                                self.reset_key(padre, min_son[0])
                                nodo_sinistro.value().clear()
                                nodo_sinistro.value().__setitem__(min_padre[0], min_padre[1])
                                self.reset_key(nodo_sinistro, min_padre[0])
                            elif son.__len__() == 1 and self._Albero.is_root(padre):
                                padre.value().__setitem__(son.find_min()[0], son.find_min()[1])
                                self._Albero.__delitem__(p.key())
                                self._Albero.__delitem__(self._Albero.right(padre).key())
                elif not self._Albero.is_leaf(p) and p.value().__len__() > 1 and p.key() > self._Albero.parent(p).key():
                    if k == p.value().find_max()[0]:
                        max_son = p.value().find_max()
                        if p.value().__getson__(max_son[0]).__len__() > 1:
                            son = p.value().__getson__(max_son[0])
                            x = son.find_max()
                            p.value().__setitem__(x[0], x[1])
                            son.__delitem__(x[0])
                            p.value().__setson__(x[0], son)
                            p.value().__delitem__(p.value().find_max()[0])
                        elif p.value().__getson__(max_son[0]).__len__() == 1 and self._Albero.right(p).value().__len__() > 1:
                            x = self._Albero.right(p).value().find_min()
                            p.value().__setitem__(x[0], x[1])
                            sons = p.value().__getson__(k)
                            it = sons.__iter__()
                            for i in it:
                                p.value().__setson__(x[0], sons)
                            p.value().__delitem__(k)
                            self._Albero.right(p).value().__delitem__(x[0])
                            self.reset_key(self._Albero.right(p), self._Albero.right(p).value().find_min()[0])
                        elif p.value().__getson__(max_son[0]).__len__() == 1 and self._Albero.right(p).value().__len__() == 1:
                            son = p.value().__getson__(max_son[0]).find_min()
                            self._Albero.right(p).value().__setitem__(son[0], son[1])
                            self.reset_key(self._Albero.right(p), son[0])
                            p.value().__delitem__(k)
                    elif k != p.value().find_max()[0] and p.key() > self._Albero.parent(p).key():
                        if p.value().__getson__(k).__len__() > 1:
                            x = p.value().__getson__(k)
                            max = x.find_max()
                            p.value().__setitem__(max[0], max[1])
                            x.__delitem__(max[0])
                            p.value().__setson__(max[0], x)
                            p.value().__delitem__(k)
                            if max[0] < k:
                                self.reset_key(p, max[0])
                        elif p.value().__getson__(k).__len__() == 1 and p.value().__getson__(p.value().find_gt(k)[0]).__len__() > 1:
                            x = p.value().__getson__(p.value().find_gt(k)[0])
                            min = x.find_min()
                            p.value().__setitem__(min[0], min[1])
                            x.__delitem__(min[0])
                            j = p.value().__getson__(k)
                            p.value().__setson__(min[0], j)
                            p.value().__delitem__(k)
                            if max[0] < k:
                                self.reset_key(p, max[0])
                elif not self._Albero.is_leaf(p) and p.value().__len__() > 1 and p.key() < self._Albero.parent(p).key():
                    if k != p.value().find_min()[0]:
                        if p.value().__getson__(k).__len__() > 1:
                            x = p.value().__getson__(k)
                            max = x.find_max()
                            p.value().__setitem__(max[0], max[1])
                            x.__delitem__(max[0])
                            p.value().__setson__(max[0], x)
                            p.value().__delitem__(k)
                        elif p.value().__getson__(k).__len__() == 1 and p.value().__getson__(p.value().find_gt(k)[0]).__len__() > 1:
                            x = p.value().__getson__(p.value().find_gt(k)[0])
                            min = x.find_min()
                            p.value().__setitem__(min[0], min[1])
                            x.__delitem__(min[0])
                            j = p.value().__getson__(k)
                            p.value().__setson__(min[0], j)
                            p.value().__delitem__(k)
            elif k_pot > k:
                if sorted.__getson__(k_pot).__len__() > 0:
                    return self.del2(k, p, sorted.__getson__(k_pot))
                else:
                    return
        else:
            return

    def stampa(self):
        iteratore3 = self._Albero.__iter__()
        c = 0
        for i in iteratore3:
            if c > 0:
                print("\n")
            c += 1
            iteratore4 = self._Albero.__getitem__(i).__iter__()  # creo un iteratore per ciascun nodo
            for j in iteratore4:
                riferimento = self._Albero.__getitem__(i).__getson__(
                    j)  # controllo se il figlio memorizzato in key,value non sia vuoto
                if riferimento.__len__() > 0:
                    print("\n")
                    iteratore5 = riferimento.__iter__()
                    for m in iteratore5:
                        print(m, riferimento.__getitem__(m))
                    print("\n")
                print(j, self._Albero.__getitem__(i).__getitem__(j))

    def getKeys(self):
        iteratore3 = self._Albero.__iter__()
        lista = []
        for i in iteratore3:
            lista.append(i)
        return lista





# #-----------------TEST----------------#
#
# abt = abTree()
#
# from Esercizio2Intracorso.Currency import Currency
#
# #----------CURRENCY INITIALIZATION-----------#
# curr1 = Currency("EUR")
# curr2 = Currency("USD")
#
# #----------CURRENCY CONSTRUCTION OBJECT----------#
# curr1.AddDenomination(0.05)
# curr1.AddDenomination(0.1)
# curr1.AddDenomination(0.2)
# curr1.AddDenomination(0.5)
# curr1.AddDenomination(1)
# curr1.AddDenomination(2)
# curr1.AddDenomination(5)
# curr1.AddDenomination(10)
# curr1.AddDenomination(20)
# curr1.AddDenomination(50)
# curr1.AddDenomination(100)
# curr1.AddDenomination(200)
# curr1.AddDenomination(500)
# curr1.addChange("USD", 1.2)
#
# curr2.AddDenomination(0.01)
# curr2.AddDenomination(0.05)
# curr2.AddDenomination(0.1)
# curr2.AddDenomination(0.25)
# curr2.AddDenomination(0.5)
# curr2.AddDenomination(1)
# curr2.AddDenomination(2)
# curr2.AddDenomination(5)
# curr2.AddDenomination(10)
# curr2.AddDenomination(20)
# curr2.AddDenomination(50)
# curr2.AddDenomination(100)
# curr2.addChange("EUR", 0.85)
#
# #------ADDING-------#
# abt.addElement(curr1._Code, curr1)
# abt.addElement(curr2._Code, curr2)
#
# #----PRINTING INITIAL RESULTS-----#
# abt.stampa()
#
# #-----SEARCHING-----#
# print("\n\n")
# print("Research results:", abt.search("EUR"))
#
# #-----DELETING------#
# abt.delete("EUR")
# print("\n\n")
#
# #----PRINTING FINAL RESULTS-----#
# abt.stampa()