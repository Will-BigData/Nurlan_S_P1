import mysql.connector
from mysql.connector import Error

def create_connection():
    print("Starting connection process...")
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="2314223Aa!",
            database="project1"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except mysql.connector.Error as mce:
        print(mce.msg)
        return None
    except Error as e:
        print(f"General error: {e}")
        return None

    return connection