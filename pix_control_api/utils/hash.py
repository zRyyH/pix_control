import hashlib
import json
import pickle


def gerar_hash(upload_file, algoritmo="sha256"):
    """
    Gera um hash criptográfico para um arquivo de upload.

    Processa o arquivo em chunks de 8KB para eficiência de memória.

    Args:
        upload_file: Objeto de arquivo de upload com atributo 'file'
        algoritmo: Nome do algoritmo de hash (padrão: "sha256")

    Returns:
        String hexadecimal contendo o hash do arquivo

    Note:
        O ponteiro do arquivo é reposicionado para o início antes da leitura
    """
    h = hashlib.new(algoritmo)
    file = upload_file.file
    file.seek(0)

    while chunk := file.read(8192):
        h.update(chunk)
    return h.hexdigest()


def gerar_hash_objeto(objeto, diferenciador=0, algoritmo="sha256"):
    """
    Gera um hash para um objeto Python de qualquer tipo.

    Args:
        objeto: Qualquer objeto Python que precisa ser hashed
        algoritmo: Algoritmo de hash a ser usado (padrão: sha256)

    Returns:
        str: Hash hexadecimal do objeto
    """

    # Cria um objeto hash com o algoritmo especificado
    h = hashlib.new(algoritmo)

    # Serializa o objeto para bytes
    try:
        # Tenta serializar como JSON para tipos nativos (dict, list, str, int, etc)
        if isinstance(objeto, (dict, list, str, int, float, bool, type(None))):
            conteudo = json.dumps(objeto, sort_keys=True).encode("utf-8")
        else:
            # Para objetos mais complexos, usa pickle
            conteudo = pickle.dumps(objeto)
    except (TypeError, pickle.PickleError):
        # Se falhar, converte para string
        conteudo = str(objeto).encode("utf-8")

    # Atualiza o hash com o conteúdo serializado
    h.update(conteudo + str(diferenciador).encode("utf-8"))

    # Retorna o hash em formato hexadecimal
    return h.hexdigest()