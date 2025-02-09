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
            logs = self.carregarLogs(self.logfile) # Carrega os logs daquele nível
            log = self.format(record)
            logs.append(log) # Adicionando o log a lista de logs
            self.salvarLogs(logs, self.logfile) # Salva o log daquele nível

    # Função para carregar logs existentes dado um arquivo de log JSON
    def carregarLogs(self, arquivo):
        try:
            with open(arquivo, 'r') as arquivo:
                return json.load(arquivo).get('logs', [])
        except FileNotFoundError as error: # Caso arquivo não exista, criá-lo
            return []
        
    # Função para salvar logs dado o arquivo de log JSON
    def salvarLogs(self, logs, arquivo):
        with open(arquivo, 'w') as arquivo:
            json.dump({"logs": logs}, arquivo, indent=2)

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

class ConfigLogger:
    def __init__(self, nome):
        self.createLogDir()

        # Logger
        self.logger = logging.getLogger(nome)
        self.logger.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

        self.createHandlers()
        self.createJSONFormatter()
        self.addFilters()

        # Adicionando Handler ao Logger
        self.logger.addHandler(self.DebugHandler)
        self.logger.addHandler(self.InfoHandler)
        self.logger.addHandler(self.WarningHandler)
        self.logger.addHandler(self.ErrorHandler)
        self.logger.addHandler(self.CriticalHandler)

    # Função para garantir que o diretório existe
    def createLogDir(self):
        logDir = './logs'
        if not os.path.exists(logDir):
            os.makedirs(logDir)
    
    def createHandlers(self):
        # Handlers
        self.DebugHandler = ListHandler(logfile='./logs/debug.json')
        self.DebugHandler.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

        self.InfoHandler = ListHandler(logfile='./logs/info.json')
        self.InfoHandler.setLevel(logging.INFO) # Setando o menor nível como o de INFO

        self.WarningHandler = ListHandler(logfile='./logs/warning.json')
        self.WarningHandler.setLevel(logging.WARNING) # Setando o menor nível como o de WARNING

        self.ErrorHandler = ListHandler(logfile='./logs/error.json')
        self.ErrorHandler.setLevel(logging.ERROR) # Setando o menor nível como o de ERROR

        self.CriticalHandler = ListHandler(logfile='./logs/critical.json')
        self.CriticalHandler.setLevel(logging.CRITICAL) # Setando o menor nível como o de CRITICAL
    
    def createJSONFormatter(self):
        # Criando formatador do Logger e adicionando-o aos Handlers do Log
        formatter = JSONFormatter()

        self.DebugHandler.setFormatter(formatter)
        self.InfoHandler.setFormatter(formatter)
        self.WarningHandler.setFormatter(formatter)
        self.ErrorHandler.setFormatter(formatter)
        self.CriticalHandler.setFormatter(formatter)

    def addFilters(self):
        # Adicionar os Filters aos handlers
        self.DebugHandler.addFilter(DebugFilter())
        self.InfoHandler.addFilter(InfoFilter())
        self.WarningHandler.addFilter(WarningFilter())
        self.ErrorHandler.addFilter(ErrorFilter())
        self.CriticalHandler.addFilter(CriticalFilter())