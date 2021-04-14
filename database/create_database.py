import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_weight(conn, weight):
    """
    Create a new weight
    :param conn:
    :param weight:
    :return:
    """

    sql = ''' INSERT INTO weights(name,value)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, weight)
    conn.commit()

    return cur.lastrowid

def create_factory(conn, factory):
    """
    Create a new factory
    :param conn:
    :param factory:
    :return:
    """

    sql = ''' INSERT INTO factories(name, latitude, longitude)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, factory)
    conn.commit()

    return cur.lastrowid

def create_warehouse(conn, warehouse):
    """
    Create a new warehouse
    :param conn:
    :param warehouse:
    :return:
    """

    sql = ''' INSERT INTO warehouses(name, latitude, longitude)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, warehouse)
    conn.commit()

    return cur.lastrowid

def main():
    database = r"database/pythonsqlite.db"

    sql_create_weights_table = """ CREATE TABLE IF NOT EXISTS weights (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        value integer NOT NULL
                                    ); """
    sql_create_factories_table = """ CREATE TABLE IF NOT EXISTS factories (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        latitude float NOT NULL,
                                        longitude float NOT NULL
                                    ); """

    sql_create_warehouses_table = """ CREATE TABLE IF NOT EXISTS warehouses (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        latitude float NOT NULL,
                                        longitude float NOT NULL
                                    ); """
    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        create_table(conn, sql_create_weights_table)
        create_table(conn, sql_create_factories_table)
        create_table(conn, sql_create_warehouses_table)
    else:
        print("Error! cannot create the database connection.")
    with conn:
        # weights = [
        #     ("gaji_rata2", 5), 
        #     ("kepadatan_penduduk", 3), 
        #     ("jarak_pabrik", 4), 
        #     ("jarak_gudang", 4),
        #     ("harga_tanah", 2)
        # ]
        # for w in weights:
        #     create_weight(conn, w)

        # factories = [
        #     ["pabrik1", -7.5, 110],
        #     ["pabrik2", -7.2, 112],
        #     ["pabrik3", -6.9, 108]
        # ]
        # for f in factories:
        #     create_factory(conn, f)

        # warehouses = [
        #     ["gudang1", -7.3, 111],
        #     ["gudang2", -7, 109]
        # ]
        # for w in warehouses:
        #     create_warehouse(conn, w)
        pass

if __name__ == '__main__':
   main()