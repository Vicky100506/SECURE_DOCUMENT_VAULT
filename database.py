import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="VIGNESH@100506",
        database="secure_vault"
    )
