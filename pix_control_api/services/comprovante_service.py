from repository.comprovante_cliente import ComprovanteClienteAPI
from repository.comprovante_empresa import ComprovanteEmpresaAPI
from processors.extractors.comprovante import extractor
from repository.configuracao import ConfiguracaoAPI
from utils.data_utils import timestamp_para_iso8601
from repository.funcionario import FuncionarioAPI
from repository.cliente import ClienteAPI
from logger import info, error, warning
import traceback


# Instancia a API do Comprovante e Cliente
comprovante_cliente_api = ComprovanteClienteAPI()

# Instancia a API do Comprovante e Empresa
comprovante_empresa_api = ComprovanteEmpresaAPI()

# Instancia a API de Configuração
configuracao_api = ConfiguracaoAPI()

# Instancia a API do Cliente
cliente_api = ClienteAPI()

# Instancia a API do Funcionario
funcionario_api = FuncionarioAPI()


def criar_comprovante_cliente(content, file, comprovante, cliente_number):
    try:
        # Obtem as configurações do sistema
        configuracao = configuracao_api.obter_configuracao()

        # Obtem cliente por numero
        cliente = cliente_api.obter_cliente_por_numero(cliente_number)

        # Verifica se o cliente existe
        if not cliente:
            warning("Cliente não encontrado, número: {}".format(cliente_number))
            return

        # Vincular comprovante ao cliente
        comprovante["cliente"] = cliente["id"]

        # Se o cliente não usa taxa global, aplica a taxa individual
        if not cliente["usa_taxa_global"]:
            comprovante["valor"] = float(comprovante["valor"]) * float(
                cliente["taxa_individual"]
            )
        else:
            comprovante["valor"] = float(comprovante["valor"]) * float(
                configuracao["taxa_global"]
            )

        # Cria o comprovante do cliente
        return comprovante_cliente_api.criar(comprovante, file, content)

    except Exception as e:
        error(f"Erro ao criar comprovante cliente {traceback.format_exc()}")
        raise Exception(f"Erro ao criar comprovante cliente")


# Função para criar comprovante de transferências bancárias
def criar_comprovante_empresa(content, file, comprovante, cliente_number, funcionario):
    try:
        # Obtem cliente por numero
        cliente = cliente_api.obter_cliente_por_numero(cliente_number)

        # Verifica se o cliente existe
        if not cliente:
            warning("Cliente não encontrado, número: {}".format(cliente_number))
            return

        # Vincular comprovante ao cliente
        comprovante["cliente"] = cliente["id"]
        comprovante["funcionario"] = funcionario["id"]

        # Cria o comprovante do cliente
        return comprovante_empresa_api.criar(comprovante, file, content)

    except Exception as e:
        error(f"Erro ao criar comprovante empresa {traceback.format_exc()}")
        raise Exception(f"Erro ao criar comprovante empresa")


# Função para validar comprovante de transferências bancárias
def processar_comprovante(content, file, message):
    try:
        info(f"Processando comprovante... {message}")

        # Extrai o texto do comprovante
        comprovante = extractor.extractor(content, file)
        info(f"Comprovante: {comprovante}")
        comprovante["data"] = timestamp_para_iso8601(message["timestamp"])

        if message["from_me"]:
            info(
                "Mensagem enviada por mim mesmo, processar comprovante empresa, cliente to_number"
            )

            funcionario = funcionario_api.obter_funcionario_por_numero(
                message["from_number"]
            )

            if not funcionario:
                warning("Seu numero não está cadastrado como funcionario")
                return False

            return criar_comprovante_empresa(
                content, file, comprovante, message["to_number"], funcionario
            )

        if message["is_group_msg"]:
            info("Mensagem é de grupo, buscar se foi enviada por funcionario")

            funcionario = funcionario_api.obter_funcionario_por_numero(
                message["author_number"]
            )

            if funcionario:
                return criar_comprovante_empresa(
                    content, file, comprovante, message["from_number"], funcionario
                )

            return criar_comprovante_cliente(
                content, file, comprovante, message["from_number"]
            )
        else:
            info("Mensagem não é de grupo")

            return criar_comprovante_cliente(
                content, file, comprovante, message["from_number"]
            )

    except Exception as e:
        error(f"Erro ao processar comprovante {traceback.format_exc()}")
        raise Exception(f"Erro ao processar comprovante")