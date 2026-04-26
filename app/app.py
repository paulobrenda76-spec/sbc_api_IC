from flask import Flask, jsonify
from flasgger import Swagger
from services.scraper_service import buscar_artigos
from database.db import criar_tabela, salvar_artigos

app = Flask(__name__)

Swagger(app)

criar_tabela()

# ROTA 1
@app.route("/artigos/<string:palavra>", methods=["GET"])
def get_artigos(palavra):
    """
    Busca artigos por palavra-chave
    ---
    parameters:
      - name: palavra
        in: path
        type: string
        required: true
        description: Palavra-chave da busca
    responses:
      200:
        description: Lista de artigos encontrados
    """
    dados = buscar_artigos(palavra)

    # DEBUG (importante agora)
    print("DADOS RECEBIDOS:", dados)

    # só salva se for lista E não estiver vazia
    if isinstance(dados, list) and len(dados) > 0:
        salvar_artigos(dados)
        print("SALVOU NO BANCO")
    else:
        print("NÃO SALVOU (dados inválidos ou vazios)")

    return jsonify(dados)


# ROTA 2
@app.route("/banco", methods=["GET"])
def listar_banco():
    """
    Lista todos os artigos salvos no banco
    ---
    responses:
      200:
        description: Lista de artigos do banco de dados
    """
    import sqlite3

    conn = sqlite3.connect("artigos.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM artigos")
    rows = cursor.fetchall()

    conn.close()

    dados = []
    for row in rows:
        dados.append({
            "id": row[0],
            "titulo": row[1],
            "autores": row[2],
            "ano": row[3],
            "link": row[4]
        })

    print("REGISTROS NO BANCO:", len(dados))

    return jsonify(dados)


if __name__ == "__main__":
    app.run(debug=True)