from constants.constants_global import EXTENSIONS
from processors.parsers.comprovante import parser
from integrations.utils_api import UtilsAPI
from logger import info, error


# Função para processar o extrato bancário
ultils_api = UtilsAPI()


# Função para processar o extrato bancário
def extractor(comprovante_content, comprovante_file):
    """
    Função para extrair transferências recebidas em extratos bancários
    """

    # Extrai a extensão do arquivo
    extension = comprovante_file.filename.split(".")[-1]

    if extension in EXTENSIONS["COMPROVANTE"]["IMAGE"]:
        comprovante_lines = ultils_api.extract_text_from_image(comprovante_content)[
            "text"
        ]["textAnnotations"][0]["description"]

    elif extension in EXTENSIONS["COMPROVANTE"]["DOCUMENT"]:
        comprovante_lines = ultils_api.extract_text_from_pdf(comprovante_content)[
            "text"
        ]

    else:
        error(f"Não suportado: {comprovante_file.filename} - {extension}")
        raise Exception("Formato de arquivo não suportado")

    # Extrai os dados importantes do comprovante
    comprovante = parser.parser(comprovante_lines)

    # Retorna o comprovante
    return comprovante
