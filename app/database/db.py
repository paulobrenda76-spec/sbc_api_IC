import psycopg2


def conectar():
    return psycopg2.connect(
        host="localhost",
        database="artigos",
        user="postgres",
        password="1234",
        port=5432
    )


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artigos (
            id SERIAL PRIMARY KEY,
            titulo TEXT NOT NULL,
            autores TEXT,
            ano INTEGER,
            link TEXT UNIQUE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()