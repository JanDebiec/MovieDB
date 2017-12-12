import db.if_functions as inf


class UserDB:
    def __init__(self, file):
        self._conn = inf.create_connection(file)

    def constructTable(self, listOfFields):
        self._cursor = inf.getCursor(self._conn)
        inf.create_table_with_one_field(listOfFields[0])
        fields = listOfFields[1:]
        for n in range (len(fields)):
            inf.add_column_with_default_value(fields[n])
        self._cursor.commit()

