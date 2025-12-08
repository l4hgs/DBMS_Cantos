import mysql.connector

def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",    # change this if needed
        database="budget_db"
    )
    return conn
