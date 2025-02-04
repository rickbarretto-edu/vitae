import zipfile
from datetime import datetime
import csv
from utils.loggers import configLogger
import os
import xml.etree.ElementTree as ET

logger = configLogger(__name__)

# Função para garantir que o diretório existe
def createCSVDir():
    csvDir = './csv'
    if not os.path.exists(csvDir):
        os.makedirs(csvDir)

def openCurriculo(curriculoZIP, subdiretorio, bufferDadosGerais, bufferProfissao, flush):
    """
    FUNÇÃO PARA ABRIR O CURRÍCULO XML DENTRO DO ARQUIVO ZIPADO

    Descrição: Recebe o currículo zipado, extrai o xml dele e faz sua leitura. Passa esse xml para outros métodos de extração
    de algumas informações úteis dos currículos

    Parâmetro: curriculoZIP - Arquivo .zip contendo o currículo lattes

    Retorno: Nenhum
    """
    logger.info(f"Processando o arquivo {curriculoZIP}")

    try:
        # Lendo arquivo zipado e abrindo o XML de dentro
        with zipfile.ZipFile(curriculoZIP, 'r') as arquivoZIP:
            nome = arquivoZIP.namelist()[0]
            idPesquisador = nome.split('.')[0] # Salvando o ID Lattes
            logger.info(f"Extraindo curriculo do pesquisador ID: {idPesquisador}")

            with arquivoZIP.open(nome) as curriculoXML:
                # Parseando o XML
                tree = ET.parse(curriculoXML)
                curriculo = tree.getroot()

                # Verificar se a pasta CSV existe. Senão, criá-la
                createCSVDir()

                #============= DADOS GERAIS ================#
                dadosGeraisPesquisador = getDadosGerais(curriculo) # Extraindo dados gerais do pesquisador e salvando em um dicionário
                dadosGeraisPesquisador["ID"] = idPesquisador # Adicionando o ID

                # Cabeçalhos do CSV
                cabeçalhos = ["ID", "DATA_ATUALIZACAO", "NOME", "CIDADE", "ESTADO", "PAIS", "NOMES_CITACOES", "ORCID", "RESUMO", "INSTITUICAO_PROFISSIONAL"]

                # Verifica se o arquivo já existe antes de abri-lo em modo de adição
                fileExist = os.path.isfile(f'./csv/dadosGerais{subdiretorio}.csv')

                bufferDadosGerais.append(dadosGeraisPesquisador)
                if flush: # Quando buffer atingir total de currículos, salvar em disco
                    with open(f'./csv/dadosGerais{subdiretorio}.csv', mode='a', newline='', encoding='utf-8') as dadosGerais:
                        writer = csv.DictWriter(dadosGerais, fieldnames=cabeçalhos)

                        if not fileExist:
                            logger.debug(f"Criando novo arquivo CSV ./csv/dadosGerais{subdiretorio}.csv")
                            writer.writeheader() # Adicionando cabeçalho
                        writer.writerows(bufferDadosGerais)
                        bufferDadosGerais.clear() # Limpa buffer
                        logger.info(f"Dados gerais do pesquisador {idPesquisador} adicionados com sucesso ao CSV.")

                #============= EXPERIÊNCIA PROFISSIONAL ================#
                experienciaProfissional = getExperienciaProfissional(curriculo)

                # Cabeçalhos do CSV
                cabeçalhos = ["ID", "INSTITUICAO", "TIPO_VINCULO", "CARGO", "ANO_INICIO", "ANO_FIM"]

                # Verifica se o arquivo já existe antes de abri-lo em modo de adição
                fileExist = os.path.isfile(f'./csv/experienciaProfissional{subdiretorio}.csv')

                for linha in experienciaProfissional:
                    bufferProfissao.append(linha)

                if flush: # Quando buffer atingir total de currículos, salvar em disco
                    with open(f'./csv/experienciaProfissional{subdiretorio}.csv', mode='a', newline='', encoding='utf-8') as dadosGerais:
                        writer = csv.DictWriter(dadosGerais, fieldnames=cabeçalhos)

                        if not fileExist:
                            logger.debug(f"Criando novo arquivo CSV ./csv/experienciaProfissional{subdiretorio}.csv")
                            writer.writeheader() # Adicionando cabeçalho
                        writer.writerows(bufferProfissao)
                        bufferProfissao.clear() # Limpa buffer
                        logger.info(f"Experiencias profissionais do pesquisador {idPesquisador} adicionadas com sucesso ao CSV.")

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo {curriculoZIP}: {str(e)}")

def getDadosGerais(curriculo):
    """
    FUNÇÃO PARA EXTRAIR ALGUNS DADOS GERAIS DO CURRÍCULO LATTES

    Descrição: Recebe o currículo XML, caminha por esse XML, salvando informações do pesquisador em variáveis

    Parâmetro: curriculo - currículo lattes de um pesquisador em XML

    Retorno: dadosGeraisPesquisador - dicionário contendo informações do pesquisador
    """
    try:
        # CV é a raiz do XML (já é o próprio `curriculo`)
        CV = curriculo

        # Busca da última data de atualização
        dataAtualizacao = CV.attrib.get("DATA-ATUALIZACAO", "")
        if dataAtualizacao:
            dataAtualizacao = datetime.strptime(dataAtualizacao, "%d%m%Y")

        # Busca da TAG de DADOS GERAIS
        dadosGerais = CV.find("DADOS-GERAIS")
        if dadosGerais is not None:
            nomeCompleto = dadosGerais.attrib.get("NOME-COMPLETO", "")
            cidadeNasc = dadosGerais.attrib.get("CIDADE-NASCIMENTO", "")
            estadoNasc = dadosGerais.attrib.get("UF-NASCIMENTO", "")
            paisNasc = dadosGerais.attrib.get("PAIS-DE-NASCIMENTO", "")
            nomesCitacoes = dadosGerais.attrib.get("NOME-EM-CITACOES-BIBLIOGRAFICAS", "")
            orcid = dadosGerais.attrib.get("ORCID-ID", "")
        else:
            nomeCompleto = cidadeNasc = estadoNasc = paisNasc = nomesCitacoes = orcid = ""

        # Busca da TAG de RESUMO
        resumoCurriculo = dadosGerais.find("RESUMO-CV")
        textoResumo = resumoCurriculo.attrib.get("TEXTO-RESUMO-CV-RH", "") if resumoCurriculo is not None else ""

        # Busca da TAG de ENDERECO
        endereco = dadosGerais.find("ENDERECO")
        if endereco is not None:
            enderecoProf = endereco.find("ENDERECO-PROFISSIONAL")
            nomeInstituicao = enderecoProf.attrib.get("NOME-INSTITUICAO-EMPRESA", "") if enderecoProf is not None else ""
        else:
            nomeInstituicao = ""

        dadosGeraisPesquisador = {
            "DATA_ATUALIZACAO": dataAtualizacao,
            "NOME": nomeCompleto,
            "CIDADE": cidadeNasc,
            "ESTADO": estadoNasc,
            "PAIS": paisNasc,
            "NOMES_CITACOES": nomesCitacoes,
            "ORCID": orcid,
            "RESUMO": textoResumo,
            "INSTITUICAO_PROFISSIONAL": nomeInstituicao
        }

        logger.debug(f"Dados gerais do pesquisador extraidos com sucesso")
        return dadosGeraisPesquisador

    except Exception as e:
        logger.error(f"Erro ao extrair dados gerais: {str(e)}")
        return {}
        
def getExperienciaProfissional(curriculo):
    """
    FUNÇÃO PARA EXTRAIR A EXPERIÊNCIA PROFISSIONAL DO CURRÍCULO LATTES

    Descrição: Recebe o currículo XML e percorre suas tags, extraindo informações das experiências profissionais.

    Parâmetro: curriculo - currículo Lattes de um pesquisador em XML.

    Retorno: experienciaProfissional - lista de dicionários contendo informações de cada experiência profissional.
    """
    try:
        # Raiz do XML
        CV = curriculo
        dadosGerais = CV.find("DADOS-GERAIS")

        # Busca da TAG de ATUAÇÕES PROFISSIONAIS
        atuacoes = dadosGerais.find("ATUACOES-PROFISSIONAIS")
        if atuacoes is None:
            return {}

        experienciaProfissional = []
        for atuacao in atuacoes.findall("ATUACAO-PROFISSIONAL"):
            instituicao = atuacao.attrib.get("NOME-INSTITUICAO", "")
            vinculos = atuacao.findall("VINCULOS")

            for vinculo in vinculos:
                tipoVinculo = vinculo.attrib.get("TIPO-DE-VINCULO", "")
                cargo = vinculo.attrib.get("OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO", "")
                anoInicio = vinculo.attrib.get("ANO-INICIO", "")
                anoFim = vinculo.attrib.get("ANO-FIM", "")

                experienciaProfissional.append({
                    "INSTITUICAO": instituicao,
                    "TIPO_VINCULO": tipoVinculo,
                    "CARGO": cargo,
                    "ANO_INICIO": anoInicio,
                    "ANO_FIM": anoFim
                })

        logger.debug(f"Experiência profissional extraída com sucesso")
        return experienciaProfissional

    except Exception as e:
        logger.error(f"Erro ao extrair experiência profissional: {str(e)}")
        return []
    
def getFormacaoAcademica(curriculo):
    """
    FUNÇÃO PARA EXTRAIR A FORMAÇÃO ACADÊMICA DO CURRÍCULO LATTES

    Descrição: Recebe o currículo XML e percorre suas tags, extraindo informações de formação acadêmica.

    Parâmetro: curriculo - currículo Lattes de um pesquisador em XML.

    Retorno: formacaoAcademica - lista de dicionários contendo informações de cada formação acadêmica.
    """
    try:
        # Raiz do XML
        CV = curriculo

        # Busca da TAG de FORMAÇÃO ACADÊMICA
        formacoes = CV.find("FORMACAO-ACADEMICA-TITULACAO")
        if formacoes is None:
            return []

        formacaoAcademica = []
        for formacao in formacoes:
            tipoFormacao = formacao.tag  # Ex: GRADUACAO, DOUTORADO, POS-DOUTORADO
            instituicao = formacao.attrib.get("NOME-INSTITUICAO", "")
            curso = formacao.attrib.get("NOME-CURSO", "")
            anoInicio = formacao.attrib.get("ANO-DE-INICIO", "")
            anoConclusao = formacao.attrib.get("ANO-DE-CONCLUSAO", "")
            tituloTrabalho = formacao.attrib.get("TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO", "")

            formacaoAcademica.append({
                "TIPO": tipoFormacao,
                "INSTITUICAO": instituicao,
                "CURSO": curso,
                "ANO_INICIO": anoInicio,
                "ANO_CONCLUSAO": anoConclusao,
                "TITULO_TRABALHO": tituloTrabalho
            })

        logger.debug(f"Formação acadêmica extraída com sucesso")
        return formacaoAcademica

    except Exception as e:
        logger.error(f"Erro ao extrair formação acadêmica: {str(e)}")
        return []
