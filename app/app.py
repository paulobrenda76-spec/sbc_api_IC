from flask import Flask, jsonify, request
from flasgger import Swagger
from services.artigo_service import ArtigoService
from database.db import criar_tabela

app = Flask(__name__)

Swagger(app, template={
    "info": {
        "title": "API de Artigos",
        "description": "API para buscar e armazenar artigos científicos",
        "version": "1.0"
    }
})

criar_tabela()

service = ArtigoService()

#ROTA 1 – buscar na API + salvar
@app.route("/artigos/<string:palavra>", methods=["GET"])
def buscar_artigos_api(palavra):
    """
    Busca artigos na API externa e salva no banco
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
    dados = service.buscar_e_salvar(palavra)
    return jsonify(dados)


#ROTA 2 – listar banco COM PAGINAÇÃO
@app.route("/banco", methods=["GET"])
def listar_banco():
    """
    Lista artigos do banco com paginação
    ---
    parameters:
      - name: page
        in: query
        type: integer
        required: false
        description: Número da página (default 1)
      - name: limit
        in: query
        type: integer
        required: false
        description: Quantidade por página (default 10)
    responses:
      200:
        description: Lista paginada de artigos
    """
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))

    return jsonify(service.listar_paginado(page, limit))


#ROTA 3 – buscar no banco
@app.route("/banco/busca/<string:titulo>", methods=["GET"])
def buscar_banco(titulo):
    """
    Busca artigos no banco pelo título
    ---
    parameters:
      - name: titulo
        in: path
        type: string
        required: true
        description: Parte do título do artigo
    responses:
      200:
        description: Lista de artigos encontrados
    """
    return jsonify(service.buscar_no_banco(titulo))

if __name__ == "__main__":
    app.run(debug=True)