import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="", ## TUA SENHA
        database="projeto-msc"
    )