from telebot import TeleBot
import requests
from bot.services.logger import setup_logger
from bot.config import WEATHER_API


# Инициализируем логгер для этого модуля
logger = setup_logger(__name__)

def setup_weather_search(bot: TeleBot):
    @bot.message_handler(commands=['weather_info'])
    def weather_search_info(message):
        '''Функция иформации о работе с API погоды'''
        chat = message.chat
        # Передаем информацию пользования ботом
        weather_info = (f'👋 Укажите город после команды <b>weather</b> и получите информацию о погоде.\n'
                        f'✅ Например, так: <code>/weather Феодосия</code>\n\n'
                        f'⚠️ <i>В случае ошибки проверьте <b>правильно написание города!</b></i>')
        
        bot.send_message(chat_id=chat.id, text=weather_info, parse_mode="HTML")


    @bot.message_handler(commands=['weather'])
    def weather_search(message):
        '''
        Функция показывает погоду в указанном городе. Дополнительно обрабатываем ошибки.
        '''
        try:
            if len(message.text.split()) < 2:
                bot.reply_to(message, "Ой-ой, кажется вы не указали город.")
                return

            # Берем все что после команды /weather(предполагается реальный город)
            city = message.text.split(maxsplit=1)[1]
            
            # Url для Api
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang=ru"
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Проверяем HTTP-ошибки

            # Если ответ не пришел отправляем ошибку
            if response.status_code != 200:
                bot.reply_to(message, f"❌ Ошибка API: {response.json()}")
                return

            weather_data = response.json() # Получаем данные в json

            # Выводи полученную информацию
            weather_info = (
                f"🌦 *Погода: {weather_data['name']}*:\n"
                f"🌡 *Температура:* {weather_data['main']['temp']}°C\n"
                f'🧊 *Ощущается как:* {weather_data['main']['feels_like']:.1f}°C\n'
                f"💨 *Ветер:* {weather_data['wind']['speed']} м/с\n"
                f"💧 *Влажность:* {weather_data['main']['humidity']}%\n"
                f"☁ *Описание:* {weather_data['weather'][0]['description'].capitalize()}"
            )
            bot.reply_to(message, weather_info, parse_mode="Markdown")

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for city: {city}")
            bot.send_message(message.chat.id, "❌ Сервер погоды не отвечает, попробуйте позже")

        except Exception as e:
            logger.error(f'API error:  {str(e)}')
            bot.send_message(message.chat.id, "❌ Произошла непредвиденная ошибка!")
