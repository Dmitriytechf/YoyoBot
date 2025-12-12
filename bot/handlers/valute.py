from telebot import TeleBot
import requests
from bot.services.logger import setup_logger
from bs4 import BeautifulSoup
from datetime import datetime 
from http import HTTPStatus
from bot.config import BRENT_API, GOLD_API

logger = setup_logger(__name__)

def setup_exchange_rate(bot: TeleBot):
    @bot.message_handler(commands=['valute'])
    def get_valute_CB(message):
        '''Получаем курсы валют от ЦБ РФ'''
        chat = message.chat
        
        try:
            url = "https://www.cbr.ru/scripts/XML_daily.asp"
            response = requests.get(url)
            response.encoding = 'windows-1251'

            # Парсим ответ
            soup = BeautifulSoup(response.text, 'lxml-xml')
            
            # Нужные валюты
            currencies = {
                'USD': 'Доллар США',
                'EUR': 'Евро'
            }
            message_text = "🏦 <b>Курсы валют ЦБ РФ</b>\n\n"
            
            for valute in soup.find_all('Valute'): # Находим по нужному тегу
                code = valute.CharCode.text # Извлекаем код валюты
                if code in currencies:
                    nominal = int(valute.Nominal.text)
                    value = float(valute.Value.text.replace(',', '.'))
                    rate = round(value / nominal, 3)
                    
                    formatted_rate = "{:,.3f}".format(rate).replace(',', ' ')
                    message_text += (
                        f"<b>{code}</b> ({currencies[code]}):\n"
                        f"✅ <b>{formatted_rate} ₽</b> за {nominal} {code}\n\n"
                    )
            
            message_text += f"🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
            
            bot.send_message(
                chat_id=message.chat.id,
                text=message_text,
                parse_mode='HTML'
            )

        except Exception as e:
            bot.send_message(chat_id=chat.id, text="⚠ Произошла ошибка при конвертации валют")
            logger.error(f'API error: {e}')
  
     
    @bot.message_handler(commands=['oil'])
    def get_oil_prices(message):
        '''Запрос к API для получения цены нефти'''
        chat = message.chat
        message_text = "<b>Курс нефти</b>\n\n"
        
        try:
            oil_url = f"https://www.alphavantage.co/query?function=BRENT&interval=daily&apikey={BRENT_API}"

            oil_response = requests.get(oil_url)
            oil_data = oil_response.json()

            if oil_response.status_code == HTTPStatus.OK and oil_data.get("data"):
                brent_price = oil_data["data"][0]["value"]
                message_text += f"🛢 <b>Нефть Brent:</b> {brent_price} $/баррель\n"

            message_text += f"\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
            
            bot.send_message(
                chat_id=chat.id,
                text=message_text,
                parse_mode='HTML'
            )

        except Exception as e:
            bot.send_message(chat_id=chat.id, text="⚠ Не удалось получить данные")
            logger.error(f'Ошибка получения API: {e}', exc_info=True)
    

    @bot.message_handler(commands=['metals'])
    def get_metals_prices(message):
        '''Получаем курс металлов'''
        chat = message.chat
        message_text = "<b>Курс драгоценных металлов</b>\n\n"
        metals = {
            'XAU': 'Золото',
            'XAG': 'Серебро', 
            'XPT': 'Платина',
            'XPD': 'Палладий'
        }
        
        try:
            headers = {"x-access-token": "goldapi-1pfsmcw3aonz-io"}
            
            for symbol, name in metals.items():
                response = requests.get(f"https://www.goldapi.io/api/{symbol}/USD", headers=headers)
                
                if response.status_code == HTTPStatus.OK:
                    price = response.json().get('price', 'N/A')
                    message_text += f"✅ <b>{name} ({symbol}):</b> {price} $/унция\n\n"
            
            message_text += f"\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
            
            bot.send_message(
                chat_id=chat.id,
                text=message_text,
                parse_mode='HTML'
            )

        except Exception as e:
            bot.send_message(chat_id=chat.id, text="⚠ Не удалось получить данные")
            logger.error(f'Ошибка получения API: {e}', exc_info=True)
    

    @bot.message_handler(commands=['crypto'])
    def crypto_rates(message):
        chat = message.chat
        
        try:            
            cryptos = {
                'bitcoin': 'Bitcoin (BTC)',
                'ethereum': 'Ethereum (ETH)',
                'the-open-network': 'TON (TON)',
                'tether': 'Tether (USDT)',
                'solana': 'Solana (SOL)',
                'ripple': 'XRP (XRP)',
                'cardano': 'Cardano (ADA)',
                'dogecoin': 'Dogecoin (DOGE)',
                'avalanche-2': 'Avalanche (AVAX)',
                'polkadot': 'Polkadot (DOT)'
            }
            ids = (',').join(cryptos.keys())
            response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd")
            data = response.json()
            
            message_text = "💰 <b>Курсы криптовалют (к USD)</b>\n\n"
            
            for crypto_id, crypto_name in cryptos.items():
                if crypto_id in data and 'usd' in data[crypto_id]:
                    price = data[crypto_id]['usd']
                    message_text += f"✅ <b>{crypto_name}</b>: {price:,.2f}$\n"
                    
            message_text += f"\n🔄 Обновлено: {datetime.now().strftime('%H:%M:%S')}"
            
            bot.send_message(
                chat_id=message.chat.id,
                text=message_text,
                parse_mode='HTML'
            )
        except Exception as e:
            bot.send_message(chat_id=chat.id, text="⚠ Не удалось получить данные о криптовалютах")
            logger.error(f'Ошибка получения API: {e}')
