from database.artigo_repository import ArtigoRepository
import csv

repo = ArtigoRepository()
dados = repo.listar_todos()

with open("artigos.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "titulo", "autores", "ano", "link"])

    for a in dados:
        writer.writerow([
            a["id"],
            a["titulo"],
            a["autores"],
            a["ano"],
            a["link"]
        ])

print("CSV gerado com sucesso!")