import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Exception as e:
        print(e)

    return None

def getCursor(connection):
    return connection.cursor()


def create_table_with_one_field(cursor, configTuple):
    table_name, field, type = configTuple[0], configTuple[1], configTuple[2]
    cursor.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf} {ft} PRIMARY KEY)'\
              .format(tn=table_name, nf=field, ft=type))
    # cursor.commit()

def add_column_with_default_value(cursor, configTuple):
    table_name, new_column, column_type, default_val = configTuple[0], configTuple[1], configTuple[2], configTuple[3]
    cursor.execute("ALTER TABLE {tn} ADD COLUMN '{cn}' {ct} DEFAULT '{df}'"\
              .format(tn=table_name, cn=new_column, ct=column_type, df=default_val))
    # cursor.commit()

def dropTable(cursor, table):
    cursor.execute("DROP TABLE {tn}".format(tn=table))


def closeDB(connection):
    connection.close()