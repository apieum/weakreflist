# -*- coding: utf8 -*-
import weakref


class WeakList(list):
    def __init__(self, items=list()):
        list.__init__(self)
        tuple(map(self.append, items))

    def get_value(self, item):
        try:
            item = item()
        finally:
            return item

    def make_ref(self, item):
        try:
            item = weakref.ref(item, self.remove)
        finally:
            return item

    def __contains__(self, item):
        return list.__contains__(self, self.make_ref(item))

    def __getitem__(self, index):
        items = list.__getitem__(self, index)
        return type(self)(map(self.get_value, items)) if isinstance(index, slice) else self.get_value(items)

    def __setitem__(self, index, item):
        items = map(self.make_ref, item) if isinstance(index, slice) else self.make_ref(item)
        return list.__setitem__(self, index, items)

    def __setslice__(self, from_index, to_index, items):
        return self.__setitem__(slice(from_index, to_index), items)

    def __iter__(self):
        return iter(self[index] for index in range(len(self)))

    def append(self, item):
        list.append(self, self.make_ref(item))

    def remove(self, item):
        item = self.make_ref(item)
        while list.__contains__(self, item):
            list.remove(self, item)

    def index(self, item):
        return list.index(self, self.make_ref(item))

    def pop(self, item):
        return list.pop(self, self.make_ref(item))
