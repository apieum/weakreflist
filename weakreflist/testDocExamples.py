# -*- coding: utf8 -*-
import unittest
from .weakreflist import WeakList
import sys
is_pypy = '__pypy__' in sys.builtin_module_names
if is_pypy:
    import gc

class DocExampleTest(unittest.TestCase):
    if not is_pypy:
        def test_example1(self):
            class A(object):
                """weakrefs don't function directly on object()"""
            objectA = A()
            my_list = WeakList([objectA])
            assert len(my_list) == 1
            del objectA
            assert len(my_list) == 0 # objectA removed from list
    else:
        def test_example2(self):
            import gc
            class A(object):
                """weakrefs don't function directly on object()"""
            objectA = A()
            my_list = WeakList([objectA])
            assert len(my_list) == 1
            del objectA

            assert len(my_list) == 1 # gc not done
            gc.collect() # must be called
            assert len(my_list) == 0
