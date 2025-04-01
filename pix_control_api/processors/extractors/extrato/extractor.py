from constants.constants_global import BANCOS
from processors.parsers.extrato import parser
from integrations.utils_api import UtilsAPI


# Função para processar o extrato bancário
ultils_api = UtilsAPI()


# Função para processar o extrato bancário
def extractor(extrato_content, banco):
    """
    Função para extrair transferências recebidas em extratos bancários
    """

    if banco == BANCOS["PINBANK"]:
        extrato_lines = ultils_api.extract_text_from_xlsx(extrato_content, start_row=2)
        return parser.parser(extrato_lines, banco)

    elif banco == BANCOS["BULLBANK"]:
        extrato_lines = ultils_api.extract_text_from_xlsx(extrato_content)
        return parser.parser(extrato_lines, banco)

    elif banco == BANCOS["ITAU"]:
        extrato_lines = ultils_api.extract_text_from_pdf(extrato_content)
        return parser.parser(extrato_lines, banco)

    elif banco == BANCOS["CORPX"]:
        extrato_lines = ultils_api.extract_text_from_pdf(extrato_content)
        return parser.parser(extrato_lines, banco)

    else:
        raise Exception("Banco não suportado")
