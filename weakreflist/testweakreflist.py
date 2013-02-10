# -*- coding: utf8 -*-
import weakref
import unittest
from weakreflist import WeakList


class WeakrefListTest(unittest.TestCase):
    class objectFake(object):
        pass

    def setUp(self):
        self.wrList = WeakList()

    def test_is_instance_of_list(self):
        self.assertIsInstance(self.wrList, list)

    def test_it_store_a_weakref_ref(self):
        myFake = self.objectFake()
        self.wrList.append(myFake)
        self.assertIsInstance(list.__getitem__(self.wrList, 0), weakref.ReferenceType)

    def test_if_a_weakref_already_stored_it_reuse_it(self):
        myFake = self.objectFake()
        self.wrList.append(myFake)
        self.wrList.append(myFake)
        self.assertEqual(list.__getitem__(self.wrList, 0), list.__getitem__(self.wrList, 1))
        self.assertEqual(self.wrList[0], self.wrList[1])

    def test_it_knows_if_it_contains_an_object(self):
        myFake0 = self.objectFake()
        myFake1 = self.objectFake()
        self.wrList.append(myFake0)
        self.assertTrue(myFake0 in self.wrList)
        self.assertFalse(myFake1 in self.wrList)

    def test_when_all_object_instance_are_deleted_all_ref_in_list_are_deleted(self):
        myFake = self.objectFake()
        self.wrList.append(myFake)
        self.wrList.append(myFake)
        self.assertEqual(2, len(self.wrList))
        del myFake
        self.assertEqual(0, len(self.wrList))

    def test_it_can_remove_a_value(self):
        myFake = self.objectFake()
        self.wrList.append(myFake)
        self.assertEqual(1, len(self.wrList))
        self.wrList.remove(myFake)
        self.assertEqual(0, len(self.wrList))

    def test_it_returns_value_and_not_a_ref(self):
        myFake = self.objectFake()
        self.wrList.append(myFake)
        self.wrList[0] = myFake
        self.assertEqual(myFake, self.wrList[0])

    def test_it_returns_the_index_of_a_value(self):
        myFake0 = self.objectFake()
        myFake1 = self.objectFake()
        self.wrList.append(myFake0)
        self.wrList.append(myFake0)
        self.wrList.append(myFake1)
        self.assertEqual(0, self.wrList.index(myFake0))
        self.assertEqual(2, self.wrList.index(myFake1))

    def test_it_support_addition(self):
        myFake = self.objectFake()
        myList = WeakList([myFake])
        self.wrList += myList
        self.assertEqual(1, len(self.wrList))

    def test_it_support_iteration(self):
        myFake = self.objectFake()
        self.wrList += [myFake, myFake, myFake, myFake]
        num_mock = 0
        for mock in self.wrList:
            num_mock += 1
            self.assertEqual(mock, myFake)
        self.assertEqual(num_mock, len(self.wrList))


if __name__ == "__main__":
    unittest.main()
