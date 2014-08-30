***********
weakreflist
***********

.. image:: https://pypip.in/v/weakreflist/badge.png
        :target: https://pypi.python.org/pypi/weakreflist

---------------------------------------------------------------------
A WeakList class for storing objects using weak references in a list.
---------------------------------------------------------------------


**Table of Contents**


.. contents::
    :local:
    :depth: 1
    :backlinks: none


=============
Installation
=============

Install it from pypi::

  pip install weakreflist

or from sources::

  git clone git@github.com:apieum/weakreflist.git
  cd weakreflist
  python setup.py install

=====
Usage
=====
Same as a *list* except that when a weakref-able variable is deleted, it is removed from the list.

**Example for CPython:**

   .. code-block:: python

      from weakref import WeakList

      class A(object):
          """weakrefs don't function directly on object()"""
      objectA = A()
      my_list = WeakList([objectA])
      assert len(my_list) == 1
      del objectA
      assert len(my_list) == 0 # objectA removed from list


*Note:*
   Pypy (probably jython, cython...) have a different implementation of garbage collector and it is known that weakrefs doesn't function the same way.

   You need to explicitly call gc.collect() which has an impact on performance.

**Example for other python implementations**

   .. code-block:: python

      from weakref import WeakList
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


===========
Development
===========

Your feedback, code review, improvements or bugs, and help to document is appreciated.
You can contact me by mail: apieum [at] gmail [dot] com

Test recommended requirements::

  pip install -r dev-requirements.txt

Sometimes --spec-color doesn't function. Uninstall nosespec and nosecolor then reinstall nosecolor and nosespec separatly in this order (nosecolor first).

Launch tests::

  git clone git@github.com:apieum/weakreflist.git
  cd weakreflist
  nosetests --with-spec --spec-color ./weakreflist
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./weakreflist



.. image:: https://secure.travis-ci.org/apieum/weakreflist.png?branch=master
   :target: https://travis-ci.org/apieum/weakreflist
