# Guia do Usuário do Vitae

Este guia é destinado a usuários não técnicos que trabalham em um ambiente já configurado.  
Se você precisa usar o Vitae sem se preocupar com instalações ou interfaces de linha de comando, este é o seu manual.

## Download

Você pode baixar a aplicação na seção **Releases** do nosso [repositório GitHub](https://github.com/lasicuefs/curricFilter).  
A aplicação é portátil, ou seja, não requer instalação.

Após o download, você verá vários arquivos na pasta.  
Os únicos arquivos que você precisa conhecer como usuário final são:

- `vitae.exe` – O lançador da aplicação.  
- `vitae.toml` – O arquivo de configuração.

## Configurando o Vitae.toml

Antes de executar o Vitae pela primeira vez, você precisará configurar alguns parâmetros do banco de dados.  
O administrador do seu sistema fornecerá esses valores.

...

Depois dessa configuração, **não** será mais necessário alterar essas configurações.

## Iniciando a Aplicação

Como qualquer outra aplicação de desktop, basta dar um duplo clique no `vitae.exe` e ela começará a funcionar.  
O carregamento completo pode levar de 5 a 7 segundos.

## Funcionalidades

![Guia](guide.png)

1. Barra de Pesquisa: Insira o nome ou ID do pesquisador  
2. Filtros: Filtrar por País, Estado, Escolaridade ou Área  
3. Enviar: Realizar a busca  
4. Ordenação: Ordenar em ordem alfabética  
5. Perfil: Clique no perfil para exportá-lo para o Lucy Lattes  
6. Perfil Externo: Abrir o perfil do pesquisador no Lattes, ou Orcid se disponível  

Navegação adicional:  
* Um botão "Carregar Mais" aparece no final da página para carregar mais resultados.  
* Um botão "Ir para o Topo" aparece do lado direito.  
* Um botão "Voltar" aparece do lado esquerdo para retornar à página anterior.

## Perguntas Frequentes

### **P:** Por que o projeto está em inglês, mas a aplicação está em português?

**R:** O projeto está em inglês para facilitar a colaboração, além de evitar ambiguidades de traduções ou termos técnicos relacionados ao projeto, pois o inglês é o idioma padrão da comunidade de desenvolvimento de software. Porém, a aplicação foi desenvolvida principalmente para usuários brasileiros, cujo idioma nativo é o português. Caso haja demanda de usuários de língua inglesa, podemos adicionar suporte completo ao inglês em versões futuras.

### **P:** O Vitae continua rodando mesmo após fechar

**R:** Na versão compilada, o backend pode continuar rodando em segundo plano após a janela ser fechada. Se isso acontecer, abra o **Gerenciador de Tarefas** do Windows, procure por `vitae.exe` e finalize o processo manualmente.
