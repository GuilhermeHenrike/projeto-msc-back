import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gilneide", ## TUA SENHA
        database="music_hub"
    )