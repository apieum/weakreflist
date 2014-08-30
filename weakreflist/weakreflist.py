# -*- coding: utf8 -*-
import weakref


class WeakList(list):
    def __init__(self, values=list()):
        list.__init__(self)
        tuple(map(self.append, values))

    def _getValue(self, ref):
        try:
            ref = ref()
        finally:
            return ref

    def _makeRef(self, value):
        try:
            value = weakref.ref(value, self.remove)
        finally:
            return value

    def __contains__(self, item):
        return list.__contains__(self, self._makeRef(item))

    def __getitem__(self, key):
        if isinstance(key, slice):
            return type(self)(self._getValue(value) for value in list.__getitem__(self, key))
        return self._getValue(list.__getitem__(self, key))

    def __getslice__(self, i, j):
        return self.__getitem__(slice(i, j))

    def __setitem__(self, key, value):
        return list.__setitem__(self, key, self._makeRef(value))

    def __iter__(self):
        return iter(self[key] for key in range(len(self)))

    def append(self, value):
        list.append(self, self._makeRef(value))

    def remove(self, value):
        value = self._makeRef(value)
        while list.__contains__(self, value):
            list.remove(self, value)

    def index(self, value):
        return list.index(self, self._makeRef(value))

    def pop(self, value):
        return list.pop(self, self._makeRef(value))
