from repository.transferencia import TransferenciaAPI
from processors.extractors.extrato import extractor
from logger import info, error


transferencia_api = TransferenciaAPI()


async def processar_extrato(extrato_file, extrato_content, banco):
    try:
        """
        Função para extrair transferências recebidas em extratos bancários
        """

        # Extrair transferências do conteúdo do extrato
        transferencias = extractor.extractor(extrato_content, banco)

        # Criar transferências no banco de dados
        result = await transferencia_api.criar_transferencias(
            transferencias, extrato_file
        )

        info(f"Total de transferências recebidas: {result}")

    except Exception as e:
        error(f"Erro ao processar extrato {extrato_file.filename} do banco {banco}")
        raise Exception(f"{str(e)}")
