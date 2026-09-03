import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Temyjd2017@", ## TUA SENHA
        database="music_hub"
    )