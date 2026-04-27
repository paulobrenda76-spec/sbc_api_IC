from database.db import conectar


class ArtigoRepository:

    def listar_todos(self):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT id, titulo, autores, ano, link FROM artigos")
        rows = cursor.fetchall()

        conn.close()

        return [
            {
                "id": r[0],
                "titulo": r[1],
                "autores": r[2],
                "ano": r[3],
                "link": r[4]
            }
            for r in rows
        ]

    def listar_paginado(self, page, limit):
        conn = conectar()
        cursor = conn.cursor()

        offset = (page - 1) * limit

        cursor.execute(
            "SELECT id, titulo, autores, ano, link FROM artigos LIMIT %s OFFSET %s",
            (limit, offset)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "titulo": r[1],
                "autores": r[2],
                "ano": r[3],
                "link": r[4]
            }
            for r in rows
        ]

    def buscar_por_titulo(self, titulo):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, titulo, autores, ano, link FROM artigos WHERE titulo ILIKE %s",
            ('%' + titulo + '%',)
        )

        rows = cursor.fetchall()
        conn.close()

        return [
            {
                "id": r[0],
                "titulo": r[1],
                "autores": r[2],
                "ano": r[3],
                "link": r[4]
            }
            for r in rows
        ]

    def existe_link(self, link):
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM artigos WHERE link = %s",
            (link,)
        )

        result = cursor.fetchone()
        conn.close()

        return result is not None

    def salvar(self, artigo):
        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO artigos (titulo, autores, ano, link)
                VALUES (%s, %s, %s, %s)
            """, (
                artigo["titulo"],
                ", ".join(artigo["autores"]),
                artigo["ano"],
                artigo["link"]
            ))

            conn.commit()

        except Exception as e:
            print("Erro ao salvar:", e)

        finally:
            conn.close()