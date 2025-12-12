from telebot import TeleBot, types
from datetime import datetime
from http import HTTPStatus
import requests
import random
from bot.services.logger import setup_logger

# Инициализируем логгер для этого модуля
logger = setup_logger(__name__)

def setup_wiki_handlers(bot: TeleBot):
    @bot.message_handler(commands=['today'])
    def history_day_today(message):
        '''Обработка API с wiki. Исторические события'''
        chat = message.chat
        today = datetime.now()
        month = today.month
        day = today.day
        
        bot.send_message(chat_id=chat.id, text=f'🎲 10 событий {today.day:02d}.{today.month:02d}')
        url = f"https://ru.wikipedia.org/api/rest_v1/feed/onthisday/events/{month}/{day}"
        response = requests.get(url)
        
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            events = data.get("events")
            random_element = random.sample(events, 10)
            
            # Делаем цикл for в пару строк с методом join()
            events_text = '\n'.join(
                f"-{event.get('year')}: {event.get('text')}" 
                for event in random_element
            )
            
            bot.send_message(chat_id=chat.id, text=events_text)
                
            
        else:
            logger.error('❌ Ошибка при запросе:', response.status_code)
            bot.send_message(chat_id=chat.id, text="Подождите, кажется у нас неполадки")     
    
            
    @bot.message_handler(commands=['holiday'])
    def holiday_day_today(message):
        '''Обработка API с wiki. Праздники'''
        chat = message.chat
        today = datetime.now()
        
        bot.send_message(chat_id=chat.id, text=f'Случайный праздник на {today.day:02d}.{today.month:02d}.\nЭто может занять какое-то время⌛️')
        
        url = f"https://ru.wikipedia.org/api/rest_v1/feed/onthisday/holidays/{today.month}/{today.day}"
        response = requests.get(url)
        
        if response.status_code == HTTPStatus.OK:
            data = response.json()
            holidays = data.get("holidays", [])
            
            if holidays:
                selected_holidays = random.sample(holidays, min(1, len(holidays)))
                holidays_text = '\n'.join(
                    f"- {holiday.get('text')[0].upper() + holiday.get('text')[1:]}" 
                    for holiday in selected_holidays)
                bot.send_message(chat_id=chat.id, text=holidays_text)
            else:
                bot.send_message(chat_id=chat.id, text='Сегодня нет известных праздников')
            
        else:
            logger.error('❌ Ошибка при запросе:', response.status_code)
            bot.send_message(chat_id=chat.id, text="Подождите, кажется у нас неполадки")