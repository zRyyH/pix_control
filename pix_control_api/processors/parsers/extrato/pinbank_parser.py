from constants.constants_global import BANCOS
import re


def parser_pinbank(extrato_content):
    transferencias = []

    # Itera sobre cada linha do conteúdo do extrato
    for row in extrato_content:
        descricao = str(row["Descrição"]).strip()

        # Remove caracteres indesejados e formata o valor
        valor = float(
            row["Valor"]
            .replace("R$", "")
            .replace(".", "")
            .replace(",", ".")
            .replace("+", "")
            .replace(" ", "")
            .strip()
        )

        # Formata a data para o padrão desejado
        data = row["Data"].replace("/", "-").strip().split(" ")[0]
        data = (
            str(re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\1/\2/\3", data))
            .strip()
            .split("-")
        )
        data = f"{data[2]}-{data[1]}-{data[0]}"

        # Verifica se a descrição contém "Crédito PIX" e extrai o nome
        match = re.search(r"Crédito PIX\s+([A-ZÁ-Úa-zá-úçÇ.\' ]+)", descricao)

        if match:
            nome = str(match.group(1)).strip()

            transferencias.append(
                {"nome": nome, "valor": valor, "data": data, "banco": BANCOS["PINBANK"]}
            )

    return transferencias