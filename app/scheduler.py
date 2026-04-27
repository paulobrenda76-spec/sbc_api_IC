import schedule
import time
from services.artigo_service import ArtigoService

#instancia do service
service = ArtigoService()


def coletar_periodicamente():
    temas = ["IA", "machine learning", "cybersecurity", "Quantum Computing", "IoT"]

    print("\nINICIANDO COLETA...")

    for tema in temas:
        print(f" Buscando: {tema}")
        try:
            artigos = service.buscar_e_salvar(tema)
            print(f"{len(artigos)} artigos processados")
        except Exception as e:
            print(f"Erro ao buscar {tema}: {e}")

    print("COLETA FINALIZADA\n")


#EXECUTA UMA VEZ AO INICIAR (IMPORTANTE PRA TESTE)
coletar_periodicamente()


#AGENDAMENTO 
schedule.every(1).hours.do(coletar_periodicamente)

print("Scheduler rodando... aguardando próximas execuções.\n")

#LOOP PRINCIPAL
while True:
    schedule.run_pending()
    time.sleep(1)