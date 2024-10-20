import time
from loguru import logger
from datetime import datetime
from functools import wraps

initial_timestamp = None

def time_log_decorator(func):
    @wraps(func)
    def wraper(*args, **kwargs):
        global initial_timestamp
        if initial_timestamp is None:
            now = datetime.now()
            initial_timestamp = now.strftime("%Y%m%d_%H%M%S")
        log_file = 'logs/municipios_'+initial_timestamp+'.log'
        logger.add(log_file, level="INFO", format="{time} {level} {message}")
        try:
            start_time = time.time()
            logger.info(f"Chamando função '{func.__name__}'")
            result = func(*args, **kwargs)
            logger.success(f"Função '{func.__name__}' execurada com sucesso")
            end_time = time.time()
            logger.info(f"Função '{func.__name__}' executada em {end_time - start_time:.4f} segundos")
            return result
        except Exception as e:
            logger.error(f"Erro ao executar a função '{func.__name__}': {e}")
            raise e
        finally:
            logger.remove()
    return wraper
    