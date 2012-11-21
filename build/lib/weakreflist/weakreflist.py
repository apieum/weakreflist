# -*- coding: utf8 -*-
import weakref


class WeakList(list):
    def _getRef(self, value):
        value = self._makeRef(value)
        if list.__contains__(self, value):
            value = list.__getitem__(self, list.index(self, value))
        return value

    def _getValue(self, ref):
        return ref()

    def _makeRef(self, value):
        try:
            value = weakref.ref(value, self.remove)
        finally:
            return value

    def __contains__(self, item):
        return list.__contains__(self, self._makeRef(item))

    def __getitem__(self, key):
        return self._getValue(list.__getitem__(self, key))

    def __setitem__(self, key, value):
        return list.__setitem__(self, key, self._getRef(value))

    def __iter__(self, *args, **kwargs):
        return list.__iter__(self, *map(self._getValue, args), **kwargs)

    def append(self, observer):
        list.append(self, self._getRef(observer))

    def remove(self, value):
        value = self._makeRef(value)
        while list.__contains__(self, value):
            list.remove(self, value)

    def index(self, *args, **kwargs):
        return list.index(self, *map(self._makeRef, args), **kwargs)

    def pop(self, value):
        return list.pop(self, self._makeRef(value))
