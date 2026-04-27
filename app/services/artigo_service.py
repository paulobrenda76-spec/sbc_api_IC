from database.artigo_repository import ArtigoRepository
from services.scraper_service import buscar_artigos
from services.arxiv_service import buscar_arxiv

class ArtigoService:

    def __init__(self):
        self.repo = ArtigoRepository()

    def buscar_e_salvar(self, palavra):
        artigos_crossref = buscar_artigos(palavra)
        artigos_arxiv = buscar_arxiv(palavra)

        todos = artigos_crossref + artigos_arxiv

        for art in todos:
            if not self.repo.existe_link(art["link"]):
                self.repo.salvar(art)

        return todos
    

    def listar_banco(self):
        return self.repo.listar_todos()

    def listar_paginado(self, page, limit):
        return self.repo.listar_paginado(page, limit)

    def buscar_no_banco(self, titulo):
        return self.repo.buscar_por_titulo(titulo)