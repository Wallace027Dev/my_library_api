from enum import Enum

class BookCategory(Enum):
    FICCAO = "Ficção"
    NAO_FICCAO = "Não Ficção"
    ROMANCE = "Romance"
    TERROR = "Terror"
    FANTASIA = "Fantasia"
    BIOGRAFIA = "Biografia"
    HISTORIA = "História"
    CIENCIA = "Ciência"
    TECNOLOGIA = "Tecnologia"
    INFANTIL = "Infantil"
    HQ_MANGAS = "HQ/Mangás"
    AUTOAJUDA = "Autoajuda"
    FILOSOFIA = "Filosofia"
    RELIGIAO = "Religião"
    NEGOCIOS = "Negócios"
    ARTE_DESIGN = "Arte e Design"
    DRAMA = "Drama"

    @classmethod
    def list(cls):
        return [e.value for e in cls]