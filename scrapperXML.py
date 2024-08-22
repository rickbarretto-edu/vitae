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

def openCurriculo(curriculoZIP="D:\\Projetos\\curricFilter\\repo\\01\\0113088308433808.zip", subdiretorio="01"):
    """
    FUNÇÃO PARA ABRIR O CURRÍCULO XML DENTRO DO ARQUIVO ZIPADO

    Descrição: Recebe o currículo zipado, extrai o xml dele e faz sua leitura. Passa esse xml para outros métodos de extração
    de algumas informações úteis dos currículos

    Parâmetro: curriculoZIP - Arquivo .zip contendo o currículo lattes

    Retorno: Nenhum
    """
    #Lendo arquivo zipado e abrindo o XML de dentro
    with zipfile.ZipFile(curriculoZIP, 'r') as arquivoZIP:
        nome = arquivoZIP.namelist()[0]
        idPesquisador = nome.split('.')[0] #Salvando o ID Lattes
        with arquivoZIP.open(nome) as curriculoXML:
            #curriculo = BeautifulSoup(curriculoXML, features="xml", from_encoding='ISO-8859-1') #Fazendo leitura do XML
            tree = ET.parse(curriculoXML)
            curriculo = tree.getroot()

            # Verificar se a pasta CSV existe. Senão, criá-la
            createCSVDir()
            
            #============= DADOS GERAIS ================#
            dadosGeraisPesquisador = getDadosGerais(curriculo) #Extraindo dados gerais do pesquisador e salvando em um dicionário
            dadosGeraisPesquisador["ID"] = idPesquisador #Adicionando o ID

            #Cabeçalhos do CSV
            cabeçalhos = ["ID", "DATA ATUALIZACAO", "NOME", "CIDADE", "ESTADO", "PAIS", "NOMES CITACOES", "ORCID", "RESUMO", "INSTITUICAO PROFISSIONAL"]
            
            # Verifica se o arquivo já existe antes de abri-lo em modo de adição
            fileExist = os.path.isfile(f'./csv/dadosGerais{subdiretorio}.csv')

            with open(f'./csv/dadosGerais{subdiretorio}.csv', mode='a', newline='', encoding='utf-8') as dadosGerais:
                writer = csv.DictWriter(dadosGerais, fieldnames=cabeçalhos)

                if not fileExist:
                    writer.writeheader() #Adicionando cabeçalho
                writer.writerow(dadosGeraisPesquisador)

def getDadosGerais(curriculo):
    """
    FUNÇÃO PARA EXTRAIR ALGUNS DADOS GERAIS DO CURRÍCULO LATTES

    Descrição: Recebe o currículo XML, caminha por esse XML, salvando informações do pesquisador em variáveis

    Parâmetro: curriculo - currículo lattes de um pesquisador em XML

    Retorno: dadosGeraisPesquisador - dicionário contendo informações do pesquisador
    """
    
    # CV é a raiz do XML (já é o próprio `curriculo`)
    CV = curriculo

    # Busca da última data de atualização
    dataAtualizacao = CV.attrib.get("DATA-ATUALIZACAO", "")
    if dataAtualizacao:
        dataAtualizacao = datetime.strptime(dataAtualizacao, "%d%m%Y")
    
    # Busca da TAG de DADOS GERAIS
    dadosGerais = CV.find("DADOS-GERAIS")
    if dadosGerais is not None:  # Se a tag existir, busca alguns atributos
        nomeCompleto = dadosGerais.attrib.get("NOME-COMPLETO", "")
        cidadeNasc = dadosGerais.attrib.get("CIDADE-NASCIMENTO", "")
        estadoNasc = dadosGerais.attrib.get("UF-NASCIMENTO", "")
        paisNasc = dadosGerais.attrib.get("PAIS-DE-NASCIMENTO", "")
        nomesCitacoes = dadosGerais.attrib.get("NOME-EM-CITACOES-BIBLIOGRAFICAS", "")
        orcid = dadosGerais.attrib.get("ORCID-ID", "")
    else:
        nomeCompleto = ""
        cidadeNasc = ""
        estadoNasc = ""
        paisNasc = ""
        nomesCitacoes = ""
        orcid = ""
    
    # Busca da TAG de RESUMO
    resumoCurriculo = dadosGerais.find("RESUMO-CV")
    if resumoCurriculo is not None:  # Se a tag existir, busca o texto do resumo
        textoResumo = resumoCurriculo.attrib.get("TEXTO-RESUMO-CV-RH", "")
    else:
        textoResumo = ""

    # Busca da TAG de ENDERECO
    endereco = dadosGerais.find("ENDERECO")
    if endereco is not None:
        # Busca da TAG de ENDERECO PROFISSIONAL
        enderecoProf = endereco.find("ENDERECO-PROFISSIONAL")
        if enderecoProf is not None:
            nomeInstituicao = enderecoProf.attrib.get("NOME-INSTITUICAO-EMPRESA", "")
        else:
            nomeInstituicao = ""
    else:
        nomeInstituicao = ""

    dadosGeraisPesquisador = {
        "DATA ATUALIZACAO": dataAtualizacao, 
        "NOME": nomeCompleto,
        "CIDADE": cidadeNasc, 
        "ESTADO": estadoNasc, 
        "PAIS": paisNasc, 
        "NOMES CITACOES": nomesCitacoes, 
        "ORCID": orcid,
        "RESUMO": textoResumo, 
        "INSTITUICAO PROFISSIONAL": nomeInstituicao
    }

    return dadosGeraisPesquisador


openCurriculo()