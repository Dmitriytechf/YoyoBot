import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from bot.config import TOKEN
from bot.exception import *
from telebot import TeleBot
from bot.handlers import (commands, numbers, wiki_events, text_handler, stickers, 
                          quotes, museum, valute, weather)
from bot.services.logger import setup_logger


project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def configure_bot():
    """Создает и настраивает экземпляр бота"""
    if not TOKEN:
        raise TokenNoneError('Токен бота не указан')
    
    try:
        bot = TeleBot(token=TOKEN)
    except Exception as e:
        raise BotCreateError(f'Ошибка при создании бота: {e}')    
        
# Регистрация обработчиков
    handlers = [
        weather.setup_weather_search,
        museum.setup_painting_museum,
        quotes.setup_random_quotes,
        valute.setup_exchange_rate,
        commands.setup_commands_handlers,
        numbers.setup_numbers_handlers,
        wiki_events.setup_wiki_handlers,
        text_handler.setup_text_handlers,
        stickers.setup_stickers_handlers
    ]
    
    for handler in handlers:
        handler(bot)
        
    return bot


def run_bot(bot, logger):
    """Запускает бота с обработкой ошибок"""  
    logger.info('БОТ ЗАПУЩЕН')
    try:
        bot.polling(none_stop=True, interval=2)
    except KeyboardInterrupt:
        logger.info(f'Бот остановлен пользователем')
    except Exception as e:
        logger.error(f'Критическая ошибка: {e}')
        raise
    finally:
        logger.info('БОТ ЗАВЕРШИЛ РАБОТУ')

 
def main():
    """Главная функция"""
    try:
        logger = setup_logger()
        bot = configure_bot()
        run_bot(bot, logger)
    except Exception as e:
        error_type = e.__class__.__name__
        logger.critical(f'Фатальная ошибка при запуске бота: {error_type}: {e}')
        sys.exit(1)

        
if __name__ == '__main__':
    main()