# -*- coding: utf8 -*-
import weakref
import unittest
from .weakreflist import WeakList
import sys
is_pypy = '__pypy__' in sys.builtin_module_names
if is_pypy:
    import gc


class WeakrefListTest(unittest.TestCase):
    class objectFake(object):
        pass

    def setUp(self):
        self.wr_list = WeakList()

    def ref_item(self, index):
        return list.__getitem__(self.wr_list, index)

    def test_it_is_instance_of_list(self):
        self.assertIsInstance(self.wr_list, list)

    def test_it_store_a_weakref_ref(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.assertIsInstance(self.ref_item(0), weakref.ReferenceType)

    def test_if_a_weakref_already_stored_it_reuse_it(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.wr_list.append(fake_obj)
        self.assertEqual(self.ref_item(0), self.ref_item(1))
        self.assertIs(self.wr_list[0], self.wr_list[1])

    def test_it_knows_if_it_contains_an_object(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.append(fake_obj0)
        self.assertTrue(fake_obj0 in self.wr_list)
        self.assertFalse(fake_obj1 in self.wr_list)

    def test_when_all_object_instance_are_deleted_all_ref_in_list_are_deleted(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.wr_list.append(fake_obj)
        self.assertEqual(2, len(self.wr_list))
        del fake_obj
        if is_pypy:
            gc.collect()
        self.assertEqual(0, len(self.wr_list))

    def test_it_can_remove_a_value(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.wr_list.append(fake_obj)
        self.assertEqual(2, len(self.wr_list))
        self.wr_list.remove(fake_obj)
        self.assertEqual(1, len(self.wr_list))

    def test_it_can_remove_all_values(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.wr_list.append(fake_obj)
        self.assertEqual(2, len(self.wr_list))
        self.wr_list.remove_all(fake_obj)
        self.assertEqual(0, len(self.wr_list))

    def test_it_can_del_a_slice(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.append(fake_obj0)
        self.wr_list.append(fake_obj0)
        self.wr_list.append(fake_obj1)
        del self.wr_list[1:]
        with self.assertRaises(IndexError):
            self.wr_list[1]
        self.assertEqual(1, len(self.wr_list))

    def test_it_returns_value_and_not_a_ref(self):
        fake_obj = self.objectFake()
        self.wr_list.append(fake_obj)
        self.wr_list[0] = fake_obj
        self.assertEqual(fake_obj, self.wr_list[0])

    def test_it_returns_the_index_of_a_value(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.append(fake_obj0)
        self.wr_list.append(fake_obj0)
        self.wr_list.append(fake_obj1)
        self.assertEqual(0, self.wr_list.index(fake_obj0))
        self.assertEqual(2, self.wr_list.index(fake_obj1))

    def test_it_supports_addition(self):
        fake_obj = self.objectFake()
        myList = WeakList([fake_obj])
        self.wr_list += myList
        self.assertEqual(1, len(self.wr_list))

    def test_it_supports_iteration(self):
        fake_obj = self.objectFake()
        self.wr_list += [fake_obj, fake_obj, fake_obj, fake_obj]
        num_mock = 0
        for mock in self.wr_list:
            num_mock += 1
            self.assertEqual(mock, fake_obj)
        self.assertEqual(num_mock, 4)

    def test_it_appends_ref_values_at_init(self):
        fake_obj = self.objectFake()
        wr_list = WeakList([fake_obj])
        self.assertEqual(1, len(wr_list))
        del fake_obj
        if is_pypy:
            gc.collect()
        self.assertEqual(0, len(wr_list))

    def test_it_supports_slice_on_int(self):
        self.wr_list = WeakList(range(10))
        self.assertEqual([self.ref_item(1), self.ref_item(2), self.ref_item(3)], self.wr_list[1:4])

    def test_it_supports_slice_on_objects(self):
        fake_obj1 = self.objectFake()
        fake_obj2 = self.objectFake()
        fake_obj3 = self.objectFake()
        fake_obj4 = self.objectFake()
        self.wr_list = WeakList([fake_obj1, fake_obj2, fake_obj3, fake_obj4])
        self.assertEqual([self.ref_item(1), self.ref_item(2)], self.wr_list[1:3])

    def test_it_can_set_slice_on_int(self):
        self.wr_list[0:] = range(3)
        self.assertEqual(self.wr_list[1:], [1, 2])
        self.assertEqual(3, len(self.wr_list))

    def test_it_can_set_slice_on_objets(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.append(fake_obj0)
        self.wr_list[1:2] = [fake_obj0, fake_obj1]
        self.assertEqual(self.ref_item(1)(), fake_obj0)
        self.assertEqual(self.ref_item(2)(), fake_obj1)
        self.assertEqual(3, len(self.wr_list))

    def test_it_can_del_slices(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list[0:] = [fake_obj0, fake_obj0, fake_obj1]
        del self.wr_list[:2]
        self.assertEqual(self.ref_item(0)(), fake_obj1)
        self.assertEqual(1, len(self.wr_list))

    def test_it_supports_extend(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.extend([fake_obj0, fake_obj0, fake_obj1])
        self.assertEqual(self.ref_item(2)(), fake_obj1)

    def test_it_supports_count(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.extend([fake_obj0, fake_obj0, fake_obj1])
        self.assertEqual(2, self.wr_list.count(fake_obj0))

    def test_it_supports_insert(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.extend([fake_obj0, fake_obj1])
        self.wr_list.insert(1, fake_obj0)
        self.assertEqual(self.ref_item(1)(), fake_obj0)
        self.assertEqual(self.ref_item(2)(), fake_obj1)

    def test_it_supports_reverse(self):
        fake_obj0 = self.objectFake()
        fake_obj1 = self.objectFake()
        self.wr_list.extend([fake_obj0, fake_obj1])
        self.wr_list.reverse()
        self.assertEqual(self.ref_item(0)(), fake_obj1)
        self.assertEqual(self.ref_item(1)(), fake_obj0)



if __name__ == "__main__":
    unittest.main()
