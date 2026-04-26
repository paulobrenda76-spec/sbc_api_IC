import requests

def buscar_artigos(palavra_chave):
    url = "https://api.crossref.org/works"

    params = {
        "query": palavra_chave,
        "rows": 10
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        return []

    data = response.json()

    artigos = []

    for item in data["message"]["items"]:
        titulo = item.get("title", ["Sem título"])[0]

        autores = []
        for a in item.get("author", []):
            nome = f"{a.get('given', '')} {a.get('family', '')}".strip()
            autores.append(nome)

        ano = None
        if "published-print" in item:
            ano = item["published-print"]["date-parts"][0][0]

        link = item.get("URL")

        artigos.append({
            "titulo": titulo,
            "autores": autores[:5],
            "ano": ano,
            "link": link
        })

    return artigos