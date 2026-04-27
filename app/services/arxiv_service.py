import requests
import xml.etree.ElementTree as ET

def buscar_arxiv(palavra_chave):
    url = f"http://export.arxiv.org/api/query?search_query=all:{palavra_chave}&start=0&max_results=10"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    root = ET.fromstring(response.text)

    artigos = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        titulo = entry.find("{http://www.w3.org/2005/Atom}title").text.strip()

        autores = []
        for author in entry.findall("{http://www.w3.org/2005/Atom}author"):
            nome = author.find("{http://www.w3.org/2005/Atom}name").text
            autores.append(nome)

        link = entry.find("{http://www.w3.org/2005/Atom}id").text

        ano = entry.find("{http://www.w3.org/2005/Atom}published").text[:4]

        artigos.append({
            "titulo": titulo,
            "autores": autores,
            "ano": int(ano),
            "link": link
        })

    return artigos