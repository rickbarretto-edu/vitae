import os
from scrapperXML import *

#pegando o caminho do primeiro subdiretório
subdiretorioPath = "D:\\Projetos\\curricFilter\\repo\\01\\" 
curriculos = os.listdir(subdiretorioPath) #lista de curriculos de cada subdiretório

#iterando a lista de curriculos
for curriculo in curriculos:
    curriculo = os.path.join(subdiretorioPath, curriculo) #pegando o caminho para o currículo Zipado
    print(curriculo)
    openCurriculo(curriculo, '01') #Chamando função de abertura de arquivo