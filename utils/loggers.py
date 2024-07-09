import logging
from pythonjsonlogger import jsonlogger
import json
import os

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

class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage(),
            'filename': record.filename,
        }
        return json.dumps(data, indent=4)

# Função para garantir que o diretório existe
def createLogDir():
    logDir = './logs'
    if not os.path.exists(logDir):
        os.makedirs(logDir)

def configLogger(nome):

    # Garantir existência do diretório LOG
    createLogDir()

    # Logger
    logger = logging.getLogger(nome)
    logger.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

    # Handlers
    DebugHandler = logging.FileHandler(filename='./logs/debug.log')
    DebugHandler.setLevel(logging.DEBUG) # Setando o menor nível como o de DEBUG

    InfoHandler = logging.FileHandler(filename='./logs/info.log')
    InfoHandler.setLevel(logging.INFO) # Setando o menor nível como o de INFO

    WarningHandler = logging.FileHandler(filename='./logs/warning.log')
    WarningHandler.setLevel(logging.WARNING) # Setando o menor nível como o de WARNING

    ErrorHandler = logging.FileHandler(filename='./logs/error.log')
    ErrorHandler.setLevel(logging.ERROR) # Setando o menor nível como o de ERROR

    CriticalHandler = logging.FileHandler(filename='./logs/critical.log')
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