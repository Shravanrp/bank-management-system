import mysql.connector

def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='bank_DBMS' #your data base name in xampp
    )