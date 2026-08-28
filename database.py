import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="senha", ## TUA SENHA
        database="music_hub"
    )