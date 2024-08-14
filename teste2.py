from utils.loggers import *

def teste2():
    logger = configLogger(__name__)

    # Gerando logs para teste
    for i in range(17):
        logger.debug(f'This is log message {i}')