import sqlite3
import os


def create_connection(db_name):
    """create a database connection to the SQLite database specified by db_name
    Parameters
    ----------
    db_name: str
        database name
    Returns
    -------
    c: connection object
        conn.cursor
    conn: connection
        direct connect to database
    """
    conn = sqlite3.connect(db_name, check_same_thread=False)

    return conn


if not os.path.exists("./database"):
    os.makedirs("./database")

connection = create_connection("./database/Woody.db")