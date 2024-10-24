import logging
import threading
import json
import os

lock = threading.Lock() # Variável de lock global

# Filtros para cada Nível de Log
class DebugFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class WarningFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING

class ErrorFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR

class CriticalFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.CRITICAL

# Handler Customizado para criar arquivo JSON
class ListHandler(logging.Handler):

    def __init__(self, logfile):
        super().__init__()
        self.logfile = logfile

    def emit(self, record): # Método acionado a cada chamada de log
        with lock:
            logs = carregarLogs(self.logfile) # Carrega os logs daquele nível
            log = self.format(record)
            logs.append(log) # Adicionando o log a lista de logs
            salvarLogs(logs, self.logfile) # Salva o log daquele nível

# Formatação JSON
class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            'timestamp': self.formatTime(record), # Data e Hora de emissão do log
            'level': record.levelname, # Nível do Log
            'message': record.getMessage(), # Mensagem do Log
            'filename': record.filename, # Arquivo que emitiu o Log
        }
        return data

# Função para carregar logs existentes dado um arquivo de log JSON
def carregarLogs(arquivo):
    try:
        with open(arquivo, 'r') as arquivo:
            return json.load(arquivo).get('logs', [])
    except FileNotFoundError as error: # Caso arquivo não exista, criá-lo
        return []

# Função para salvar logs dado o arquivo de log JSON
def salvarLogs(logs, arquivo):
    with open(arquivo, 'w') as arquivo:
        json.dump({"logs": logs}, arquivo, indent=2)

# Função para garantir que o diretório existe
def createLogDir():
    logDir = './logs'
    if not os.path.exists(logDir):
        os.makedirs(logDir)

# Função para configuração do Logger, seus Handlers, Formatters e Filters
def configLogger(nome):

    # Garantir existência do diretório LOG
    createLogDir()

    # Logger
    logger = logging.getLogger(nome)
    logger.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

    # Handlers
    DebugHandler = ListHandler(logfile='./logs/debug.json')
    DebugHandler.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

    InfoHandler = ListHandler(logfile='./logs/info.json')
    InfoHandler.setLevel(logging.INFO) # Setando o menor nível como o de INFO

    WarningHandler = ListHandler(logfile='./logs/warning.json')
    WarningHandler.setLevel(logging.WARNING) # Setando o menor nível como o de WARNING

    ErrorHandler = ListHandler(logfile='./logs/error.json')
    ErrorHandler.setLevel(logging.ERROR) # Setando o menor nível como o de ERROR

    CriticalHandler = ListHandler(logfile='./logs/critical.json')
    CriticalHandler.setLevel(logging.CRITICAL) # Setando o menor nível como o de CRITICAL

    # Criando formatador do Logger e adicionando-o aos Handlers do Log
    formatter = JSONFormatter()
    DebugHandler.setFormatter(formatter)
    InfoHandler.setFormatter(formatter)
    WarningHandler.setFormatter(formatter)
    ErrorHandler.setFormatter(formatter)
    CriticalHandler.setFormatter(formatter)

    # Adicionar os Filters aos handlers
    DebugHandler.addFilter(DebugFilter())
    InfoHandler.addFilter(InfoFilter())
    WarningHandler.addFilter(WarningFilter())
    ErrorHandler.addFilter(ErrorFilter())
    CriticalHandler.addFilter(CriticalFilter())

    # Adicionando Handler ao Logger
    logger.addHandler(DebugHandler)
    logger.addHandler(InfoHandler)
    logger.addHandler(WarningHandler)
    logger.addHandler(ErrorHandler)
    logger.addHandler(CriticalHandler)

    return logger