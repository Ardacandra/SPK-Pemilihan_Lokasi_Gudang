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

def select_all_weights(conn):
    """
    Query all rows in the weights table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM weights")

    rows = cur.fetchall()
    print("Weights fetched")
    return rows

def update_weights(conn, weights):
    """
    update value dari weights
    :param conn:
    :param weights:
    :return: project id
    """
    for i in range(len(weights)):
        sql = ''' UPDATE weights
                SET value = ?
                WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, [weights[i], i+1])
        conn.commit()
    
def select_all_factories(conn):
    """
    Query all rows in the factories table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM factories")

    rows = cur.fetchall()
    print("Factories fetched")
    return rows

def select_all_warehouses(conn):
    """
    Query all rows in the warehouses table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM warehouses")

    rows = cur.fetchall()
    print("Warehouses fetched")
    return rows