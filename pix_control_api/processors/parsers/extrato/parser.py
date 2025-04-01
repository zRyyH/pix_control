from constants.constants_global import BANCOS
from processors.parsers.extrato import (
    itau_parser,
    bullbank_parser,
    corpx_parser,
    pinbank_parser,
)


# Função para processar o extrato bancário
def parser(extrato_content, banco):
    if banco == BANCOS["PINBANK"]:
        return pinbank_parser.parser_pinbank(extrato_content)

    elif banco == BANCOS["BULLBANK"]:
        return bullbank_parser.parser_bullbank(extrato_content)

    elif banco == BANCOS["ITAU"]:
        return itau_parser.parser_itau(extrato_content)

    elif banco == BANCOS["CORPX"]:
        return corpx_parser.parser_corpx(extrato_content)

    else:
        raise Exception("Banco não suportado")
