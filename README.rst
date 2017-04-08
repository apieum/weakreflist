***********
weakreflist
***********
--------------------------------------------------------------------
A WeakList class for storing objects using weak references in a list
--------------------------------------------------------------------

.. image:: https://pypip.in/v/weakreflist/badge.png
  :target: https://pypi.python.org/pypi/weakreflist

**Table of Contents**

.. contents::
   :local:
   :depth: 1
   :backlinks: none


============
Installation
============

Install it from PyPi::

  pip install weakreflist

or from Github::

  git clone git@github.com:apieum/weakreflist.git
  cd weakreflist
  python setup.py install


=====
Usage
=====

``WeakList`` provides the same methods as the built-in ``list`` but will remove any ``weakref``-compatible objects that
are released by the garbage collector.


**Example for CPython:**

  .. code-block:: python

    from weakreflist import WeakList

    class A(object):
        """weakrefs don't function directly on object()"""

    objectA = A()
    my_list = WeakList([objectA])
    assert len(my_list) == 1
    del objectA
    assert len(my_list) == 0 # objectA removed from list


*Note:*
  Pypy has a different implementation of garbage collection which changes some behavior of ``weakref``.
  This may be true in other 3\ :superscript:`rd`-party compilers such as Jython and Cython. 
  Some interactive interpreters, like IPython, `may also delay calls to <http://stackoverflow.com/a/12023927/1993468>`_
  ``gc``.

  Due to this, you will need to explicitly call ``gc.collect()`` which has a negative impact on performance!

**Example for other Python implementations**

  .. code-block:: python

    from weakreflist import WeakList
    import gc

    class A(object):
        """weakrefs don't function directly on object()"""

    objectA = A()
    my_list = WeakList([objectA])
    assert len(my_list) == 1
    del objectA

    assert len(my_list) == 1 # gc did not run
    gc.collect() # must be called explicitly
    assert len(my_list) == 0


===========
Development
===========

Your feedback, code review, improvements, bug reports, and help to document is appreciated.
You can contact me by email: apieum [at] gmail [dot] com

Setup
-----

Install recommended packages for running tests::

  pip install -r dev-requirements.txt

*Note:*
  Sometimes `--spec-color` doesn't function. This can potentially be fixed by the following:

  #. Uninstall ``nosespec`` and ``nosecolor``
  #. Reinstall ``nosecolor`` alone
  #. Reinstall ``nosespec``

  Be certain to reinstall them separately and in the order given, otherwise you will continue
  to experience the same issue!

Run tests
---------

::

  git clone git@github.com:apieum/weakreflist.git
  cd weakreflist
  nosetests --with-spec --spec-color ./weakreflist
  # or with watch
  # nosetests --with-spec --spec-color --with-watch ./weakreflist


============
Contributors
============

Thanks to `BoonsNaibot <https://github.com/BoonsNaibot>`_ for the following contributions:
  * extended slicing support
  * `__reversed__`, `count`, `extend`, and `insert` methods.



.. image:: https://secure.travis-ci.org/apieum/weakreflist.png?branch=master
  :target: https://travis-ci.org/apieum/weakreflist
