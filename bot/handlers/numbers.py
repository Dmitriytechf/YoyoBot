from telebot import TeleBot
import requests
from bot.services.logger import setup_logger
from bot.services.translator import TextTranslator

# Инициализируем логгер для этого модуля
logger = setup_logger(__name__)

def setup_numbers_handlers(bot: TeleBot):
    @bot.message_handler(commands=['numfact'])
    def random_num_fact(message):
        '''Работа с Numbers API'''
        chat = message.chat
        
        try:
            num =   message.text.split()
            
            if len(num) > 1:
                number = num[1]
                url = f'http://numbersapi.com/{number}?json'
            else:
                url = 'http://numbersapi.com/random?json'
            
            response = requests.get(url) # Передаем полученный url
            
            fact_data = response.json()
            fact = fact_data['text']
            # Переводим на русский
            translated = TextTranslator.translate_to_russian(fact)
            
            bot.send_message(chat_id=chat.id, text=f'Оригинал: {fact}')
            bot.send_message(chat_id=chat.id, text=f'Перевод: {translated}')
        
        except IndexError:
            bot.send_message(chat_id=chat.id, 
                            text=f'{chat.first_name}, введите команду /numfact и после число.')

        except Exception as e:
            bot.send_message(chat_id=chat.id, text="Произошла ошибка при получении факта о числе")
            logger.error(f'API error: {e}')

        bot.send_message(chat_id=chat.id, text=f'Еще вы можете добавить к команде число (к примеру, /numfact 42) и получите факты по нему.')
        
