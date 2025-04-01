from repository.comprovante_cliente import ComprovanteClienteAPI
from repository.comprovante_empresa import ComprovanteEmpresaAPI
from processors.extractors.comprovante import extractor
from repository.configuracao import ConfiguracaoAPI
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


# Função para validar comprovante de transferências bancárias
def processar_comprovante(content, file, from_number, to_number):
    try:
        # Obtem funcionário por numero
        funcionario = funcionario_api.obter_funcionario_por_numero(from_number)

        # Verifica se o arquivo é um comprovante
        configuracao = configuracao_api.obter_configuracao()

        # Extrai o texto do comprovante
        comprovante = extractor.extractor(content, file)

        if funcionario and str(from_number) == funcionario["numero"]:
            cliente = cliente_api.obter_cliente_por_numero(to_number)
            if not cliente:
                warning(f"Cliente não encontrado, número: {to_number}")
                return
            
            comprovante["cliente"] = cliente["id"]
            comprovante["funcionario"] = funcionario["id"]
            result = comprovante_empresa_api.criar(comprovante, file, content)

        else:
            cliente = cliente_api.obter_cliente_por_numero(from_number)
            if not cliente:
                warning(f"Cliente não encontrado, número: {from_number}")
                return
            comprovante["cliente"] = cliente["id"]

            if not cliente["usa_taxa_global"]:
                comprovante["valor"] = float(comprovante["valor"]) * float(
                    cliente["taxa_individual"]
                )
            else:
                comprovante["valor"] = float(comprovante["valor"]) * float(
                    configuracao["taxa_global"]
                )

            result = comprovante_cliente_api.criar(comprovante, file, content)

        info(f"Comprovante criado: {result}")

    except Exception as e:
        error(f"Erro ao processar comprovante {traceback.format_exc()}")
        raise Exception(f"Erro ao processar comprovante")
