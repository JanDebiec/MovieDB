import csv
import sys
import os

# from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from sqlalchemy.orm import mapper, create_session

from numbers import Number
from collections import Set, Mapping, deque

# class ManagedFile:
#     def __init__(self, name, mode = 'r'):
#         self._name = name
#         self._mode = mode
#
#     def __enter__(self):
#         self._file = open(self._name,self._mode)
#         return self._file
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         if self._file:
#             self._file.close()
#
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

# def csvToDbTable(csvFile):
#     engine = create_engine('sqlite://')  # memory-only database
#
#     table = None
#     metadata = MetaData(bind=engine)
#     with ManagedFile(csvFile) as f:
#         # assume first line is header
#         cf = csv.DictReader(f, delimiter=',')
#         for row in cf:
#             if table is None:
#                 # create the table
#                 table = Table('foo', metadata,
#                               Column('id', Integer, primary_key=True),
#                               *(Column(rowname, String()) for rowname in row.keys()))
#                 table.create()
#             # insert data into the table
#             table.insert().values(**row).execute()
#     return table
#

def line_binary_search(filename, matchvalue, key=lambda val: val):
    """
    Binary search a file for matching lines.
    Returns a list of matching lines.
    filename - path to file, passed to 'open'
    matchvalue - value to match
    key - function to extract comparison value from line

    >>> parser = lambda val: int(val.split('\t')[0].strip())
    >>> line_binary_search('sd-arc', 63889187, parser)
    ['63889187\t3592559\n', ...]
    """

    # Must be greater than the maximum length of any line.

    max_line_len = 2 ** 12

    start = pos = 0
    end = os.path.getsize(filename)

    with open(filename, 'rb') as fptr:
        # Limit the number of times we binary search.

        for rpt in xrange(50):
            last = pos
            pos = start + ((end - start) / 2)
            fptr.seek(pos)

            # Move the cursor to a newline boundary.

            fptr.readline()
            line = fptr.readline()
            linevalue = key(line)

            if linevalue == matchvalue or pos == last:

                # Seek back until we no longer have a match.

                while True:
                    fptr.seek(-max_line_len, 1)
                    fptr.readline()
                    if matchvalue != key(fptr.readline()):
                        break

                # Seek forward to the first match.

                for rpt in xrange(max_line_len):
                    line = fptr.readline()
                    linevalue = key(line)
                    if matchvalue == linevalue:
                        break
                else:
                    # No match was found.

                    return []

                results = []

                while linevalue == matchvalue:
                    results.append(line)
                    line = fptr.readline()
                    linevalue = key(line)

                return results
            elif linevalue < matchvalue:
                start = fptr.tell()
            else:
                assert linevalue > matchvalue
                end = fptr.tell()
        else:
            raise RuntimeError('binary search failed')