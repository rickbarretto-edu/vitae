import os
from scrapperXML import openCurriculo
from utils.loggers import configLogger
from concurrent.futures import ThreadPoolExecutor

# Configuração do logger
logger = configLogger(__name__)

# Função para realizar a varredura do diretório de currículos
def scanning():
    """
    VARRE O DIRETÓRIO DE CURRÍCULOS LATTES E BUSCA TODOS OS CURRÍCULOS ZIPADOS

    Descrição: Caminha o diretório atual até os arquivos ZIPs e chama a 
    função openCurriculo(curriculo) passando como parâmetro o currículo zipado.

    Parâmetro: Nenhum

    Retorno: Nenhum
    """
    try:
        diretorioAtual = os.getcwd()  # Pegando o diretório atual
        logger.info(f"Diretorio atual: {diretorioAtual}")

        diretorioCurriculos = os.path.join(diretorioAtual, "repo")  # Diretório dos currículos
        listaDeSubDiretorios = os.listdir(diretorioCurriculos)  # Lista de subdiretórios

        # Log do início do processo de varredura
        logger.info(f"Subdiretorios encontrados em {diretorioCurriculos}: {listaDeSubDiretorios}")

        with ThreadPoolExecutor(max_workers=12) as executor:
            # Iterando sobre os subdiretórios
            for subdiretorio in listaDeSubDiretorios:
                subdiretorioPath = os.path.join(diretorioCurriculos, subdiretorio)  # Caminho de cada subdiretório
                print(subdiretorioPath)
                executor.submit(processarSubDir, subdiretorioPath) # Executando

        logger.info("Varredura completa de todos os subdiretórios.")
    except Exception as e:
        logger.error(f"Ocorreu um erro durante a varredura: {e}")

def processarSubDir(subdiretorio):
    curriculos = os.listdir(subdiretorio)  # Lista de currículos no subdiretório

    logger.info(f"Processando subdiretorio: {subdiretorio} com {len(curriculos)} curriculos")

    buffer = []  # Buffer para armazenar os dados dos currículos processados
    flush = False # Variável que indica se o buffer pode passar seus dados para o disco

    # Iterando sobre os currículos
    for curriculo in curriculos:
        curriculoPath = os.path.join(subdiretorio, curriculo)  # Caminho para o currículo ZIP
        logger.debug(f"Abrindo curriculo: {curriculoPath}")
        print(curriculo)
        if curriculo == curriculos[-1]: # Se for o último currículo, pode dar flush no buffer
            flush = True
        openCurriculo(curriculoPath, subdiretorio, buffer, flush)  # Processando o currículo

    # Aqui você pode realizar o processamento final com o buffer, como salvar em disco
    logger.info(f"Subdiretorio {subdiretorio} processado com sucesso.")
    buffer.clear()  # Limpa o buffer após processar os currículos do subdiretório

# Chamando a função scanning()
scanning()
