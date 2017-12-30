import io
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

class ManagedUtfFile:
    def __init__(self, name, mode = 'r', encoding='UTF-8'):
        self._name = name
        self._mode = mode
        self._encoding = encoding

    def __enter__(self):
        self._file = io.open(self._name,mode=self._mode, encoding=self._encoding, errors='replace')
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

