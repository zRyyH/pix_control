from integrations.directus_api import DirectusAPI
from logger import info, error


# Classe para manipular clientes na API do Directus
class ClienteAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def obter_cliente_por_numero(self, numero):
        try:
            cliente = self.directus_api.get_directus(
                endpoint="/items/clientes",
                params={"filter[numero][_eq]": numero},
            )["data"]

            if not cliente:
                return None

            return cliente[0]

        except Exception as e:
            error(f"Erro ao obter cliente por numero, numero: {numero}, erro: {str(e)}")
            raise Exception(f"Erro ao obter cliente por numero")
