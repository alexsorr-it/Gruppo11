from StruttureDati.hash_table.hash_map_base import MapBase
from random import randrange
import sympy



class HashMapBase(MapBase):
  """Abstract base class for map using hash-table with MAD compression.

  Keys must be hashable and non-None.
  """

  def __init__(self, cap=17, p=109345121):
    """Create an empty hash-table map.

    cap     initial table size (default 11)
    p       positive prime used for MAD (default 109345121)
    """
    self._table = cap * [ None ]
    self._n = 0                                   # number of entries in the map
    self._prime = p                               # prime for MAD compression
    self._scale = 1 + randrange(p-1)              # scale from 1 to p-1 for MAD
    self._shift = randrange(p)                    # shift from 0 to p-1 for MAD

  def _hash_function(self, k):
    return (hash(k)*self._scale + self._shift) % self._prime % len(self._table)

  def __len__(self):
    return self._n

  def __getitem__(self, k):
    j = self._hash_function(k)
    return self._bucket_getitem(j, k)             # may raise KeyError

  def __setitem__(self, k, v):
    j = self._hash_function(k)
    self._bucket_setitem(j, k, v)                 # subroutine maintains self._n
    if self._n > len(self._table) // 2:           # keep load factor <= 0.5
      v = 2 * len(self._table) - 1
      if sympy.isprime(v):
          self._resize(v)
      else:
          self._resize(sympy.nextprime(v))

  def __delitem__(self, k):
    j = self._hash_function(k)
    self._bucket_delitem(j, k)                    # may raise KeyError
    self._n -= 1
    if self._n < len(self._table)//5:           # keep load factor >= 0.2
      v = len(self._table)//2 - 1
      if sympy.isprime(v):
          self._resize(v)
      else:
          self._resize(sympy.nextprime(v))

  def _resize(self, c):
    """Resize bucket array to capacity c and rehash all items."""
    old = list(self.items())       # use iteration to record existing items
    self._table = c * [None]       # then reset table to desired capacity
    self._n = 0                    # n recomputed during subsequent adds
    for (k,v) in old:
      self[k] = v                  # reinsert old key-value pair



class DoubleHashingHashMap(HashMapBase):
    # "””Hash table implemented with linear probing.”””
    _AVAIL = object()  # sentinel marking positions of previous deletions

    def __init__(self):
        super().__init__()
        self._c = 0

    def _is_available(self, j):
        # Return True if cell with index j is free.
        return self._table[j] is None or self._table[j] is DoubleHashingHashMap._AVAIL

    def _hash_function2(self, k):
        return 3 - (hash(k) % 3)

    def _find_slot(self, j, k, check):
        firstAvail = None
        m = self._hash_function2(k)
        while True:
            if self._is_available(j):
                if firstAvail is None:
                    firstAvail = j  # mark the cell as the first available
                if self._table[j] is None:
                    return (False, firstAvail)  # search failed
            elif k == self._table[j]._key:
                return (True, j)  # found a match
            j = j + m
            j = (j) % len(self._table) # keep looking
            if check:
                self._c += 1

    def _getCollisions(self):
        return self._c

    def _bucket_getitem(self, j, k):
        found, x = self._find_slot(j, k, False)
        if not found:
            raise KeyError('Key Error: ' + repr(k)) # key not found
        return self._table[x]._value

    def _bucket_setitem(self, j, k, v):
        if k.isupper() and (len(k) == 3):
            found, x = self._find_slot(j, k, True)
            if not found:
                self._table[x] = self._Item(k, v)  # insert a new element
                self._n += 1  # increases size
            else:
                self._table[x]._value = v  # overwrite the old value
        else:
            raise KeyError('Key Format Error: keys must be of three upper capital letter' + repr(k))

    def _bucket_delitem(self, j, k):
        found, x = self._find_slot(j, k, False)
        if not found:
            raise KeyError('Key Error: ' + repr(k))  # key not found
        self._table[x] = DoubleHashingHashMap._AVAIL  # mark cell as empty

    def __iter__(self):
        for j in range(len(self._table)):  # scan the entire table
            if not self._is_available(j):
                yield self._table[j]._key