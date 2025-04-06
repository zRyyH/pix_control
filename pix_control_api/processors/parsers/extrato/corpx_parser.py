from constants.constants_global import BANCOS
import re


def parser_corpx(extrato_content):
    texto = extrato_content

    texto = re.sub(r"\n", " ", texto)

    # Regex ajustado para o formato específico do extrato
    padrao = r"(\d{2}/\d{2}/\d{4})TRANS RECEBIDA PIX - ([^-]+)-([^R]+)R\$ ([\d\.,]+) C"

    # Encontrar todas as ocorrências
    transferencias = re.findall(padrao, texto)

    # Formatar os resultados
    resultados = []
    for data, nome, cpf_cnpj, valor in transferencias:
        valor = float(valor.replace(".", "").replace(",", "."))
        data = data.split("/")
        data = str(f"{data[2]}-{data[1]}-{data[0]}")

        resultados.append(
            {
                "data": data,
                "nome": nome.strip(),
                "valor": valor,
                "banco": BANCOS["CORPX"],
            }
        )

    return resultados
