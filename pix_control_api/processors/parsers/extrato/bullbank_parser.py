from constants.constants_global import BANCOS


def parser_bullbank(extrato_content):
    transferencias = []

    for row in extrato_content:
        nome = str(row["Customer Name"]).strip()
        valor = float(row["Amount"])
        data = str(row["Datetime (America/Sao_Paulo)"].split(" ")[0]).strip()

        if row["Type"] != "inbound" or row["Method"] != "pix":
            continue

        transferencias.append(
            {"nome": nome, "valor": valor, "data": data, "banco": BANCOS["BULLBANK"]}
        )

    return transferencias
