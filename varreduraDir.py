import os
from scrapperXML import openCurriculo
from utils.loggers import configLogger

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

        # Iterando sobre os subdiretórios
        for subdiretorio in listaDeSubDiretorios:
            subdiretorioPath = os.path.join(diretorioCurriculos, subdiretorio)  # Caminho de cada subdiretório
            curriculos = os.listdir(subdiretorioPath)  # Lista de currículos no subdiretório

            logger.info(f"Processando subdiretorio: {subdiretorio} com {len(curriculos)} curriculos")

            buffer = []  # Buffer para armazenar os dados dos currículos processados

            # Iterando sobre os currículos
            for curriculo in curriculos:
                curriculoPath = os.path.join(subdiretorioPath, curriculo)  # Caminho para o currículo ZIP
                logger.debug(f"Abrindo curriculo: {curriculoPath}")
                openCurriculo(curriculoPath, subdiretorio, buffer)  # Processando o currículo

            # Aqui você pode realizar o processamento final com o buffer, como salvar em disco
            logger.info(f"Subdiretorio {subdiretorio} processado com sucesso. Limpeza do buffer.")
            buffer.clear()  # Limpa o buffer após processar os currículos do subdiretório

            # Removendo o break para varrer todos os subdiretórios
            # break  # TEMPORÁRIO: Use para processar apenas um subdiretório para testes

        logger.info("Varredura completa de todos os subdiretórios.")
    except Exception as e:
        logger.error(f"Ocorreu um erro durante a varredura: {e}")

# Chamando a função scanning()
scanning()
