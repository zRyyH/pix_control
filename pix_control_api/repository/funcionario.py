from integrations.directus_api import DirectusAPI
from logger import info, error


# Classe para manipular funcionarios na API do Directus
class FuncionarioAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def obter_funcionario_por_numero(self, numero):
        try:
            funcionario = self.directus_api.get_directus(
                endpoint="/items/funcionarios",
                params={"filter[numero][_eq]": numero},
            )["data"]

            if not funcionario:
                return None

            return funcionario[0]

        except Exception as e:
            error(
                f"Erro ao obter funcionario por numero, numero: {numero}, erro: {str(e)}"
            )
            raise Exception(f"Erro ao obter funcionario por numero")
