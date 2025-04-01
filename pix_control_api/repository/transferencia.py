from integrations.strapi_api_3 import run_bulk_requests
from utils.hash import gerar_hash_objeto, gerar_hash


class TransferenciaAPI:
    """
    Classe para fazer upload de transferências no Strapi
    """

    async def criar_transferencias(self, transferencias, extrato_file):
        try:
            requests = []

            # Gera o hash do arquivo de extrato
            extrato_hash = gerar_hash(extrato_file)

            for index, transf in enumerate(transferencias):
                # Gera o hash do objeto de transferência e do extrato
                hash_file_index = gerar_hash_objeto(extrato_hash, index)

                transf.update({"extrato_hash": hash_file_index})

                requests.append(
                    ("post", ("/api/transferencias",), {"json": {"data": transf}})
                )

            return await run_bulk_requests(requests, max_concurrency=500)

        except Exception as e:
            raise Exception(f"Erro ao criar transferencia: {str(e)}")
