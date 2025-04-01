from integrations.directus_api import DirectusAPI
from utils.hash import gerar_hash
from logger import info, error


class ComprovanteEmpresaAPI:
    def __init__(self):
        self.directus_api = DirectusAPI()

    def _verificar_hash(self, file):
        try:
            # Gera o hash do arquivo
            file_hash = gerar_hash(file)

            # Busca o comprovante no banco de dados
            response = self.directus_api.get_directus(
                endpoint="/items/comprovantes_empresa",
                params={"filter[hash][_eq]": file_hash},
            )["data"]

            info(
                f"Verificando hash do comprovante empresa, hash: {file_hash}, response: {response}"
            )

            # Verifica se o comprovante já existe
            if response and len(response) > 0:
                return True
            return False

        except Exception as e:
            error(f"Erro ao verificar hash comprovante empresa: {str(e)}")
            raise Exception(f"Erro ao verificar hash comprovante empresa")

    def criar(self, data, file, content):
        try:
            if self._verificar_hash(file):
                info("Comprovante empresa já existe no banco de dados")
                raise Exception("Comprovante empresa já existe no banco de dados")

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
                endpoint="/items/comprovantes_empresa",
                json=data,
            )

            info("Fazendo upload do comprovante empresa")

        except Exception as e:
            error(f"Erro ao fazer upload do comprovante empresa: {str(e)}")
            raise Exception(f"Erro ao fazer upload do comprovante empresa")
