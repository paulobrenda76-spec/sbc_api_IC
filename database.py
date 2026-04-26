import sqlite3

def conectar():
    return sqlite3.connect("artigos.db")

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autores TEXT,
            ano INTEGER,
            link TEXT UNIQUE
        )
    """)

    conn.commit()
    conn.close()


def salvar_artigos(lista_artigos):
    conn = conectar()
    cursor = conn.cursor()

    for art in lista_artigos:
        try:
            cursor.execute("""
                INSERT INTO artigos (titulo, autores, ano, link)
                VALUES (?, ?, ?, ?)
            """, (
                art["titulo"],
                ", ".join(art["autores"]),  
                art["ano"],
                art["link"]
            ))
        except:
            
            continue

    conn.commit()
    conn.close()