from integrations.directus_api import DirectusAPI
from utils.hash_utils import gerar_hash
from logger import info, error, warning


class ComprovanteClienteAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def _verificar_hash(self, file):
        try:
            # Gera o hash do arquivo
            file_hash = gerar_hash(file)

            # Busca o comprovante no banco de dados
            response = self.directus_api.get_directus(
                endpoint="/items/comprovantes_cliente",
                params={"filter[hash][_eq]": file_hash},
            )["data"]

            info(
                f"Verificando hash do comprovante cliente, hash: {file_hash}, response: {response}"
            )

            # Verifica se o comprovante já existe
            if response and len(response) > 0:
                return True
            return False

        except Exception as e:
            error(f"Erro ao verificar hash comprovante cliente: {str(e)}")
            raise Exception(f"Erro ao verificar hash comprovante cliente")

    def criar(self, data, file, content):
        try:
            if self._verificar_hash(file):
                warning(
                    "Comprovante cliente já existe no banco de dados, operação cancelada"
                )
                return False

            arquivo = self.directus_api.post_directus(
                endpoint="/files",
                files={
                    "file": (
                        file.filename,
                        content,
                        file.content_type,
                    )
                },
            )["data"]

            data.update(
                {
                    "hash": gerar_hash(file),
                    "arquivo": arquivo["id"],
                }
            )

            self.directus_api.post_directus(
                endpoint="/items/comprovantes_cliente",
                json_data=data,
            )

            return True

        except Exception as e:
            error(f"Erro ao fazer upload do comprovante cliente: {str(e)}")
            raise Exception(f"Erro ao fazer upload do comprovante cliente")

    def obter_comprovantes(self, params=None):
        try:
            # Obtem todos os comprovantes do cliente
            return self.directus_api.get_directus(
                endpoint="/items/comprovantes_cliente",
                params=params,
            )["data"]

        except Exception as e:
            error(f"Erro ao obter comprovantes cliente: {str(e)}")
            raise Exception(f"Erro ao obter comprovantes cliente")
