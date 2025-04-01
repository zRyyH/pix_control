from constants.constants_global import BANCOS
import re


def parser_itau(extrato_content):
    texto = extrato_content["text"]

    # Regex que não depende do mês específico
    padrao = r"PIX TRANSF ([A-Za-z\s\.]+?)(\d{2}/\d{2}) ([\d\.,]+)"

    # Encontrar todas as ocorrências
    matches = re.findall(padrao, texto)

    # Processar e formatar os resultados
    resultados = []
    for match in matches:
        nome, data, valor = match
        nome = str(nome).strip()
        valor = float(valor.replace(".", "").replace(",", "."))
        data = f"{data}/2025".split("/")
        data = f"{data[2]}-{data[1]}-{data[0]}"

        resultados.append(
            {"nome": nome, "data": data, "valor": valor, "banco": BANCOS["ITAU"]}
        )

    return resultados
