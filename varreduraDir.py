import os
from scrapperXML import *
#import cProfile

def scanning():
    """
    VARRE O DIRETÓRIO DE CURRÍCULOS LATTES E BUSCA TODOS OS CURRÍCULOS ZIPADOS

    Descrição: Caminha o diretório atual até os arquivo zips e chama a 
    função openCurriculo(curriculo) passando como parâmetro o currículo zipado

    Parâmetro: Nenhum

    Retorno: Nenhum
    """
    diretorioAtual = os.getcwd() #pegando o diretório atual

    diretorioCurriculos = os.path.join(diretorioAtual, "repo") #pegando o diretório dos currículos
    listaDeSubDiretorios = os.listdir(diretorioCurriculos) #gerando lista de subdiretórios para serem iteradas

    #iterando lista de subdiretorios
    for subdiretorio in listaDeSubDiretorios:
        subdiretorioPath = os.path.join(diretorioCurriculos, subdiretorio) #pegando o caminho de cada subdiretório
        curriculos = os.listdir(subdiretorioPath) #lista de curriculos de cada subdiretório

        #iterando a lista de curriculos
        for curriculo in curriculos:
            curriculo = os.path.join(subdiretorioPath, curriculo) #pegando o caminho para o currículo Zipado
            print(curriculo)
            openCurriculo(curriculo, subdiretorio) #Chamando função de abertura de arquivo

        break #BREAK temporário só para percorrer até o subdiretório 01

#cProfile.run('scanning()', 'profilingET.prof') # Rodar o scanning com a varredura de um único subdiretório de currículos (01)
scanning()