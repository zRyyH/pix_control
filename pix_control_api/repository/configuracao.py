from integrations.directus_api import DirectusAPI
from logger import info, error


# Classe para manipular clientes na API do Directus
class ConfiguracaoAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def obter_configuracao(self):
        try:
            configuracao = self.directus_api.get_directus(
                endpoint="/items/configuracao",
            )["data"]

            if not configuracao:
                return None

            info(f"Configuração encontrada, id_configuracao: {configuracao['id']}")

            return configuracao

        except Exception as e:
            error(f"Erro ao obter configuração, erro: {str(e)}")
            raise Exception(f"Erro ao obter configuração")
