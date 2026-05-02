import schedule
import time
import csv
import os
from services.artigo_service import ArtigoService

service = ArtigoService()

ARQUIVO_CSV = "artigos_sociais.csv"


def gerar_temas_sociais():
    temas_base = [
        "racial inequality",
        "racial justice",
        "anti racism",
        "feminism",
        "gender equality",
        "women empowerment",
        "LGBT rights",
        "LGBT discrimination",
        "anti LGBT discrimination",
        "social justice",
        "human rights",
        "minority rights",
        "diversity and inclusion",
        "intersectionality",
        "gender studies"
    ]

    contextos = [
        "education", "workplace", "technology",
        "healthcare", "law", "public policy"
    ]

    temas = []

    for base in temas_base:
        for ctx in contextos:
            temas.append(f"{base} in {ctx}")
            temas.append(f"{base} research")
            temas.append(f"{base} analysis")

    return list(set(temas))


def salvar_em_csv(artigos):
    arquivo_existe = os.path.isfile(ARQUIVO_CSV)

    with open(ARQUIVO_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not arquivo_existe:
            writer.writerow(["id", "titulo", "autores", "ano", "link", "texto"])

        for art in artigos:
            writer.writerow([
                art.get("id", ""),
                art.get("titulo", ""),
                art.get("autores", ""),
                art.get("ano", ""),
                art.get("link", ""),
                (art.get("texto", "")[:3000] if art.get("texto") else "")
            ])


def coletar_sociais():
    temas = gerar_temas_sociais()

    print("\nINICIANDO COLETA SOCIAL...")

    for tema in temas[:50]:
        print(f"Buscando: {tema}")

        try:
            artigos = service.buscar_e_salvar(tema)

            if artigos:
                salvar_em_csv(artigos)

            print(f"{len(artigos)} artigos")

        except Exception as e:
            print(f"Erro: {e}")

        time.sleep(2)

    print("COLETA FINALIZADA\n")


coletar_sociais()

schedule.every(1).minutes.do(coletar_sociais)

print("Scheduler social rodando...\n")

while True:
    schedule.run_pending()
    time.sleep(1)