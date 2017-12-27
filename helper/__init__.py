import os
import csv
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table

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

def csvToDbTable(csvFile, delimiter):
    engine = create_engine('sqlite://')  # memory-only database

    table = None
    metadata = MetaData(bind=engine)
    with ManagedFile(csvFile) as f:
        # assume first line is header
        cf = csv.DictReader(f, delimiter=delimiter)
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

def findLineWithId(filename, matchId, delimiter='\t'):
    '''binary search in TSV files from IMDB'''
    start = 0
    end = os.path.getsize(filename)
    with ManagedFile(filename) as fptr:

        while (start < end):
            pos = start + ((end - start) / 2)

            fptr.seek(pos)
            fptr.readline()
            line = fptr.readline()
            values = line.split(sep=delimiter)
            firstValue = values[0]
            lineId = firstValue[2:]# ignore the first 2 chars
            if matchId == lineId:
                return line
            elif matchId > lineId:
                start = fptr.tell()
            else:
                end = fptr.tell()
        return []

