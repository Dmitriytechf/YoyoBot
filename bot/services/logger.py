import logging

def setup_logger(name=__name__):
    '''Настройка и возврат логгера'''
    logger = logging.getLogger(name)
    
    if not logger.handlers:  # Чтобы не дублировать обработчики
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger