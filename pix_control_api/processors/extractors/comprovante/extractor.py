from integrations.google_cloud import extract_text_from_image
from utils.pdf_utils import extract_text_from_pdf
from constants.constants_global import EXTENSIONS
from processors.parsers.comprovante import parser
from logger import error


# Função para processar o extrato bancário
def extractor(comprovante_content, comprovante_file):
    """
    Função para extrair transferências recebidas em extratos bancários
    """

    # Extrai a extensão do arquivo
    extension = comprovante_file.filename.split(".")[-1]

    if extension in EXTENSIONS["COMPROVANTE"]["IMAGE"]:
        comprovante_lines = extract_text_from_image(comprovante_content)[
            "textAnnotations"
        ][0]["description"]

    elif extension in EXTENSIONS["COMPROVANTE"]["DOCUMENT"]:
        comprovante_lines = extract_text_from_pdf(comprovante_content)

    else:
        error(f"Não suportado: {comprovante_file.filename} - {extension}")
        raise Exception("Formato de arquivo não suportado")

    # Extrai os dados importantes do comprovante
    comprovante = parser.parser(comprovante_lines)

    # Retorna o comprovante
    return comprovante
