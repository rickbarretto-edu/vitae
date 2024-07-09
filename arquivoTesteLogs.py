from utils.loggers import *

def teste1():
    logger = configLogger(__name__)

    # Gerando logs para teste
    for i in range(3):
        logger.error(f'This is log message {i}')