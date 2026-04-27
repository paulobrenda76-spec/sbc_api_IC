import requests

def buscar_artigos(palavra_chave):
    url = "https://api.crossref.org/works"

    params = {
        "query": palavra_chave,
        "rows": 10
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Erro ao acessar API:", e)
        return []

    data = response.json()

    artigos = []

    for item in data.get("message", {}).get("items", []):

        titulo = item.get("title", ["Sem título"])
        titulo = titulo[0] if titulo else "Sem título"

        autores = []
        for a in item.get("author", []):
            nome = f"{a.get('given', '')} {a.get('family', '')}".strip()
            if nome:
                autores.append(nome)

        ano = None
        if "published-print" in item:
            try:
                ano = item["published-print"]["date-parts"][0][0]
            except:
                pass

        link = item.get("URL")

        # evita salvar lixo
        if not link:
            continue

        artigos.append({
            "titulo": titulo,
            "autores": autores[:5],
            "ano": ano,
            "link": link
        })

    return artigos