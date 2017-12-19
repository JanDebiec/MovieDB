import csv
import sys
import os

from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import mapper, create_session

from numbers import Number
from collections import Set, Mapping, deque

class ManagedFile:
    def __init__(self, name, mode = 'r'):
        self._name = name
        self._mode = mode

    def __enter__(self):
        self._file = open(self._name,self._mode)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()

class inputCsvReader:
    def __init__(self, file):
        self._file = file


    def __enter__(self):
        self._reader = csv.reader(self._file)
        return self._reader

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._reader:
            self._reader.close()

    def getInputAsList(self):
        return list(self._reader)



try: # Python 2
    zero_depth_bases = (basestring, Number, xrange, bytearray)
    iteritems = 'iteritems'
except NameError: # Python 3
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'

def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    def inner(obj, _seen_ids = set()):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size
    return inner(obj_0)

def csvToDbTable(csvFile):
    engine = create_engine('sqlite://')  # memory-only database

    table = None
    metadata = MetaData(bind=engine)
    with ManagedFile(csvFile) as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=',')
        for row in cf:
            if table is None:
                # create the table
                table = Table('foo', metadata,
                              Column('id', Integer, primary_key=True),
                              *(Column(rowname, String()) for rowname in row.keys()))
                table.create()
            # insert data into the table
            table.insert().values(**row).execute()
    return table