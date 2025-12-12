from telebot import TeleBot
import requests
from bot.services.logger import setup_logger
from bot.services.translator import TextTranslator
import random
from config import LOTR_API


logger = setup_logger(__name__)

def setup_random_quotes(bot: TeleBot):
    @bot.message_handler(commands=['randomquote'])
    def get_random_quote(message):
        '''Случайные цитаты с API Forismatic'''
        chat = message.chat
        
        try:
            response = requests.get(
            'http://api.forismatic.com/api/1.0/',
                params={
                    'method': 'getQuote',
                    'format': 'json',
                    'lang': 'ru'
                }
            )
            response.raise_for_status()
            data = response.json()
            
            bot.send_message(chat_id=chat.id, 
                             text=f"{data['quoteText']}\n(c) {data['quoteAuthor'] or 'Неизвестный автор'}"
                             )
            
        except Exception as e:
            logger.error (f"Не удалось получить цитату. Ошибка: {e}")
            
    @bot.message_handler(commands=['stoickquote'])
    def get_filosofia_quote(message):
        '''Случайные цитаты с API Stoic Quotes'''
        chat = message.chat
        
        try:
            response = requests.get(
            'https://stoic-quotes.com/api/quote'
            )
            response.raise_for_status()
            data = response.json()
            text = data['text']
            author = data['author']
            
            # Переводим цитату и автора, импортируя класс TextTranslator с папки services
            translated_text = TextTranslator.translate_to_russian(text)
            translated_author = TextTranslator.translate_to_russian(author)
            
            bot.send_message(chat_id=chat.id, 
                             text=f"Оригинал:\n{data['text']}\n(c) {data['author']}")
            bot.send_message(chat_id=chat.id, 
                             text=f"Перевод:\n{translated_text}\n(c) {translated_author}")
            
        except Exception as e:
            logger.error (f"Не удалось получить цитату. Ошибка: {e}")
                    
    @bot.message_handler(commands=['LOTRquote'])
    def get_lotr_quote(message):
        '''Случайные цитаты с The One API'''
        chat = message.chat
        
        try:
            headers = {
                'Authorization': f'Bearer {LOTR_API}'
            }
            response = requests.get(
                'https://the-one-api.dev/v2/quote',
                headers=headers
            )
            quote_data = response.json()
            
            random_quote = random.choice(quote_data['docs'])
            quote_text = random_quote['dialog']
            character_id = random_quote['character']
            
            character_response = requests.get(
                f'https://the-one-api.dev/v2/character/{character_id}',
                headers=headers
            )
            character_data = character_response.json()
            character_name = character_data['docs'][0]['name']
            
            translated_text = TextTranslator.translate_to_russian(quote_text )
            
            bot.send_message(chat_id=chat.id, 
                            text=f"{character_name}: «{quote_text}»(оригинал)"
                            )
            
            bot.send_message(chat_id=chat.id, 
                            text=f"{character_name}: «{translated_text}»(перевод)"
                            )
        except Exception as e:
            logger.error (f"Не удалось получить цитату. Ошибка: {e}")
        
        
        