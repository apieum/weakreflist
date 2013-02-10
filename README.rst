===========
weakreflist
===========
---------------------------------------------------------------------
A WeakList class for storing objects using weak references in a list.
---------------------------------------------------------------------

*usage*
 see tests::
 
   # cd weakreflist
   # nosetests --with-spec --spec-color ./
 
   Weakref list
   - if a weakref already stored it reuse it
   - it can remove a value
   - it is instance of list
   - it knows if it contains an object
   - it returns the index of a value
   - it returns value and not a ref
   - it store a weakref ref
   - it support addition
   - it support iteration
   - when all object instance are deleted all ref in list are deleted

   ----------------------------------------------------------------------
   Ran 10 tests in 0.004s
   
   OK