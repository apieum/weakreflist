# -*- coding: utf8 -*-
from weakref import ref
from collections import Sequence

class WeakList(list):

    def __init__(self, items=None):
        items = items or []
        super(WeakList, self).__init__((ref(x, self._remove) for x in items))

    def __contains__(self, item):
        return super(WeakList, self).__contains__(ref(item, self._remove))

    def __getitem__(self, i):
        if not isinstance(i, slice):
            return super(WeakList, self).__getitem__(i)()
        gen = (x() for x in super(WeakList, self).__getitem__(i))
        return list(gen)

    def __getslice__(self, i, j):
        s = slice(i, j, None)
        return self.__getitem__(s)

    def __iter__(self):
        for x in super(WeakList, self).__iter__():
            yield x()

    def __repr__(self):
        return "WeakList({!r})".format(list(self))

    def __reversed__(self, *args, **kwargs):
        for x in super(WeakList, self).__reversed__(*args, **kwargs):
            yield x()

    def __setitem__(self, i, item):
        if not isinstance(i, slice):
            super(WeakList, self).__setitem__(i, ref(item, self._remove))
            return
        gen = (ref(x, self._remove) for x in item)
        super(WeakList, self).__setitem__(i, gen)

    def __setslice__(self, i, j, items):
        s = slice(i, j, None)
        if not isinstance(items, Sequence):
            items = (items,)
        self.__setitem__(s, items)

    def _remove(self, item):
        while super(WeakList, self).__contains__(item):
            super(WeakList, self).remove(item)

    def append(self, item):
        super(WeakList, self).append(ref(item, self._remove))

    def count(self, item):
        return super(WeakList, self).count(ref(item, self._remove))

    def extend(self, items):
        super(WeakList, self).extend((ref(x, self._remove) for x in items))

    def index(self, item):
        return super(WeakList, self).index(ref(item, self._remove))

    def insert(self, i, item):
        super(WeakList, self).insert(i, ref(item, self._remove))
        
    def pop(self, i=-1):
        return super(WeakList, self).pop(i)()

    def remove(self, item):
        super(WeakList, self).remove(ref(item, self._remove))
