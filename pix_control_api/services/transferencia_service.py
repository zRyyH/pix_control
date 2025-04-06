from repository.comprovante_cliente import ComprovanteClienteAPI
from repository.transferencia import TransferenciaAPI
from integrations.bullbank_api import BullBankAPI
from logger import info, error, warning
import traceback


bullbank_api = BullBankAPI()
transferencias_api = TransferenciaAPI()
comprovante_cliente_api = ComprovanteClienteAPI()


def buscar_comprovante_correspondente(transferencia):
    """
    Verifica se a transferência é válida com base nos comprovantes existentes.
    """

    params = {
        "filter[nome]": transferencia["nome"].strip().upper(),
        "filter[valor]": transferencia["valor"],
        "filter[transferencias_id][_null]": True,
    }

    comprovantes = comprovante_cliente_api.obter_comprovantes(params=params)

    if comprovantes:
        return comprovantes[0]


def obter_transferencias_elegiveis():
    try:
        """
        Filtra as transferências elegíveis com base nos critérios definidos.
        """
        transferencias_elegiveis = []

        # Obtem as transferências do BullBank
        transferencias = bullbank_api.obter_transferencias()["transactions"]

        for transferencia in transferencias:
            isStatus = transferencia["status"] == "succeeded"
            isType = transferencia["type"] == "inbound"
            isMethod = transferencia["method"] == "pix"

            if isStatus and isType and isMethod:
                transferencias_elegiveis.append(transferencia)

        return transferencias_elegiveis

    except Exception as e:
        error(f"Erro ao filtrar transferências elegíveis {traceback.format_exc()}")
        raise Exception(f"Erro ao filtrar transferências elegíveis")


def formatar_transferencia_bullbank(transferencia):
    """
    Formata as transferências para o formato esperado pela API.
    """
    try:
        return {
            "id_bullbank": transferencia["id"],
            "nome": transferencia["payerName"].strip().upper(),
            "valor": float(transferencia["amountCents"]) / 100,
            "data": transferencia["completedAt"],
        }

    except Exception as e:
        error(f"Erro ao formatar transferência {traceback.format_exc()}")
        raise Exception(f"Erro ao formatar transferência")


def atualizar_transferencia(id, transferencia):
    """
    Atualiza a transferência na API do Directus.
    """
    try:
        comprovante = buscar_comprovante_correspondente(transferencia)

        if comprovante:
            transferencia["comprovante_cliente_id"] = comprovante["id"]

            info(
                f"Transferência atualizada: {transferencia['comprovante_cliente_id']:<15} - {transferencia['id_bullbank']:>75}"
            )

        return transferencias_api.update(id, transferencia)

    except Exception as e:
        error(f"Erro ao atualizar transferência {traceback.format_exc()}")
        raise Exception(f"Erro ao atualizar transferência")


def processar_transferencias():
    try:
        info("Iniciando processamento de transferências...")

        transferencias_elegiveis = obter_transferencias_elegiveis()

        for transferencia_bullbank in transferencias_elegiveis:
            transferencia_directus = transferencias_api.get_by_id_bullbank(
                transferencia_bullbank["id"]
            )

            transferencia_bullbank = formatar_transferencia_bullbank(
                transferencia_bullbank
            )

            if transferencia_directus:
                atualizar_transferencia(
                    transferencia_directus[0]["id"], transferencia_bullbank
                )
            else:
                transferencias_api.create(transferencia_bullbank)
                info(f"Transferência criada: {transferencia_bullbank['id_bullbank']}")

        info(
            f"Processamento de transferências concluído. Total: {len(transferencias_elegiveis)}"
        )
        return True

    except Exception as e:
        error(f"Erro ao processar transferências {traceback.format_exc()}")
        raise Exception(f"Erro ao processar transferências")
