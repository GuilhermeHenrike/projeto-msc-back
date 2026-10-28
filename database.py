import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ny2005ny", ## TUA SENHA
        database="music_hub"
    )