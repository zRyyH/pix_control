from integrations.utils_api import UtilsAPI
from logger import error, info


# Instancia a API do Utils
utils_api = UtilsAPI()


# Função para processar o extrato bancário
def parser(comprovante_content):
    try:
        message = """
        Me retorne um JSON no formato:
        {
        "nome": nome de quem enviou str, 
        "valor": valor transferido float, 
        "data": data da transferência nesse formato yyyy-mm-dd str
        }"""

        # Extrai os dados importantes do texto
        data = utils_api.extract_important_data(comprovante_content + message)["text"]

        # Verifica se o JSON é válido
        comprovante = {
            "nome": data["nome"],
            "valor": data["valor"],
            "data": data["data"],
        }

        # Retorna o comprovante
        return comprovante

    except Exception as e:
        error(f"Erro ao processar o comprovante: {str(e)}")
        raise Exception(f"Erro ao processar o comprovante: {str(e)}")
