import db.if_functions as inf


# dbStruct = [(table_name,field,type),
#             (table_name,new_column,column_type,default_val),
#             ]

class UserDB:
    def __init__(self, file):
        self._file = file

    def __enter__(self):
        self._conn = inf.create_connection(self._file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            self._conn.close()

    def constructTable(self, listOfFields):
        self._cursor = inf.getCursor(self._conn)
        inf.create_table_with_one_field(self._cursor,listOfFields[0])
        self._conn.commit()
        fields = listOfFields[1:]
        for n in range (len(fields)):
            inf.add_column_with_default_value(self._cursor,fields[n])
            self._conn.commit()

    def addField(self, fieldStruct):
        inf.add_column_with_default_value(self._cursor, fieldStruct)
        self._conn.commit()

    def close(self):
        self._conn.close()

    def dropTable(self, table):
        inf.dropTable(self._cursor,table)
        self._conn.commit()