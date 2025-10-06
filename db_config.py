import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Praj77258@',
        database='inventory_db'
    )
    return conn