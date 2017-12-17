import db.if_functions as inf


# dbStruct = [(table_name,field,type),
#             (table_name,new_column,column_type,default_val),
#             ]

class UserDB:
    def __init__(self, file):
        self._conn = inf.create_connection(file)

    def constructTable(self, listOfFields):
        self._cursor = inf.getCursor(self._conn)
        inf.create_table_with_one_field(self._cursor,listOfFields[0])
        fields = listOfFields[1:]
        for n in range (len(fields)):
            inf.add_column_with_default_value(self._cursor,fields[n])
        self._conn.commit()

