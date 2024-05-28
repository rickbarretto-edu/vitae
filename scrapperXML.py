import zipfile
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

#DataFrames pandas a serem atualizados com os dados e exportados
dfGerais = pd.DataFrame(columns=["ID", "DATA ATUALIZACAO", "NOME", "CIDADE", "ESTADO", "PAIS", "NOMES CITACOES", "ORCID", 
    "RESUMO", "INSTITUICAO PROFISSIONAL"])

def exportCSV(dicionarioDF):
    """
    FUNÇÃO PARA EXPORTAR DATAFRAMES PANDAS PARA CSV

    Descrição: Recebe um dicionario de dataframes pandas e exporta cada um para um csv

    Parâmetro: dicionarioDF - dicionário contendo dataframes pandas.

    Retorno: Nenhum
    """

    dicionarioDF["DADOS GERAIS"].to_csv('./csv/dadosGerais.csv', index=False)
    #Acrescentar resto das exportações dos outros dicionarios

def adicionarLinha(df, linha):
    """
    FUNÇÃO PARA ADICIONAR UMA NOVA LINHA (REGISTRO) A UM DATAFRAME PANDAS

    Descrição: Recebe um dataframe e adiciona uma nova linha a ele

    Parâmetro: df - DataFrame pandas
    Parâmetro: linha - dicionário a ser incrementado ao DataFrame

    Retorno: df - DataFrame atualizado
    """
    novaLinha = pd.DataFrame([linha])
    df = pd.concat([df, novaLinha], ignore_index=True)
    return df

def openCurriculo(curriculoZIP):
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
        curriculoXML = arquivoZIP.open(nome)

    curriculo = BeautifulSoup(curriculoXML, features="xml", from_encoding='ISO-8859-1') #Fazendo leitura do XML

    #DADOS GERAIS
    dadosGeraisPesquisador = getDadosGerais(curriculo) #Extraindo dados gerais do pesquisador e salvando em um dicionário
    dadosGeraisPesquisador["ID"] = idPesquisador #Adicionando o ID
    global dfGerais
    dfGerais = adicionarLinha(dfGerais, dadosGeraisPesquisador) #Adicionando o registro a um dataframe

    #OUTRO MÉTODO PARA EXTRAIR AQUI

    dicionarioDF = {"DADOS GERAIS": dfGerais}
    exportCSV(dicionarioDF)

def getDadosGerais(curriculo):
    """
    FUNÇÃO PARA EXTRAIR ALGUNS DADOS GERAIS DO CURRÍCULO LATTES

    Descrição: Recebe o currículo XML, caminha por esse XML, salvando informações do pesquisador em variáveis

    Parâmetro: curriculo - currículo lattes de um pesquisador em XML

    Retorno: dadosGeraisPesquisador - dicionário contendo informações do pesquisador
    """
    
    CV = curriculo.find_all("CURRICULO-VITAE") #Pega toda a árvore do currículo

    #Verifica se há somente um currículo no XML
    if(len(CV) != 1):
        return -1
    else: #Se existir UM currículo

        #Busca da última data de atualização
        dataAtualizacao = curriculo.find("CURRICULO-VITAE")["DATA-ATUALIZACAO"]
        dataAtualizacao = datetime.strptime(dataAtualizacao, "%d%m%Y")

        #Busca da TAG de DADOS GERAIS
        dadosGerais = curriculo.find("DADOS-GERAIS")
        if(dadosGerais != None): #Se a tag existir, busca alguns atributos
            nomeCompleto = dadosGerais.get("NOME-COMPLETO", "")
            cidadeNasc = dadosGerais.get("CIDADE-NASCIMENTO", "")
            estadoNasc = dadosGerais.get("UF-NASCIMENTO", "")
            paisNasc = dadosGerais.get("PAIS-DE-NASCIMENTO", "")
            nomesCitacoes = dadosGerais.get("NOME-EM-CITACOES-BIBLIOGRAFICAS", "")
            orcid = dadosGerais.get("ORCID-ID", "")
        else:
            nomeCompleto = ""
            cidadeNasc = ""
            estadoNasc = ""
            paisNasc = ""
            nomesCitacoes = ""
            orcid = ""
    
        #Busca da TAG de RESUMO
        resumoCurriculo = curriculo.find("RESUMO-CV")
        if(resumoCurriculo != None): #Se a tag existir, busca o texto do resumo
            textoResumo = resumoCurriculo.get("TEXTO-RESUMO-CV-RH", "")
        else:
            textoResumo = ""

        #Busca da TAG de ENDERECO
        endereco = curriculo.find("ENDERECO")
        if(endereco != None):
            #Busca da TAG de ENDERECO PROFISSIONAL
            enderecoProf = endereco.find("ENDERECO-PROFISSIONAL")
            if(enderecoProf != None):
                nomeInstituicao = endereco.get("NOME-INSTITUICAO-EMPRESA", "")
            else:
                nomeInstituicao = ""
        else:
            nomeInstituicao = ""

    dadosGeraisPesquisador = {"DATA ATUALIZACAO": dataAtualizacao, "NOME": nomeCompleto, 
    "CIDADE": cidadeNasc, "ESTADO": estadoNasc, "PAIS": paisNasc, "NOMES CITACOES": nomesCitacoes, "ORCID": orcid, 
    "RESUMO": textoResumo, "INSTITUICAO PROFISSIONAL": nomeInstituicao}

    return dadosGeraisPesquisador