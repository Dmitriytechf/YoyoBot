class BotError(Exception):
    '''Базовый класс для всех ошибок бота.'''

class TokenNoneError(BotError):
    '''Ошибка: токен не указан или невалиден.'''

class BotCreateError(BotError):
    '''Ошибка при создании бота.'''
