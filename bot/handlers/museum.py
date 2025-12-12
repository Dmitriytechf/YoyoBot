from telebot import TeleBot
import requests
from bot.services.logger import setup_logger
from bot.services.translator import TextTranslator
import random


logger = setup_logger(__name__)

def setup_painting_museum(bot: TeleBot):
    @bot.message_handler(commands=['gallery'])
    def get_painting_museum_random(message):
        chat = message.chat
        bot.send_message(chat_id=chat.id, 
                             text=f"@{chat.username}, подождите, мы загружаем произведения искусства...")
        
        random_skip = random.randint(0, 1000)
        response = requests.get(
            "https://openaccess-api.clevelandart.org/api/artworks/",
            params={
                "limit": 1,
                "has_image": 1,
                "skip": random_skip 
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if data["data"]: 
            artwork = data["data"][0]
            image_url = artwork["images"]["web"]["url"]
            title = artwork.get("title", "Без названия")
            creator = (
                artwork.get("creators", [{}])[0].get("description", "Неизвестный автор") 
                if artwork.get("creators") 
                else "Неизвестный автор"
            )
            
            translated_title = TextTranslator.translate_to_russian(title)
        
            bot.send_photo(
                chat.id,
                photo=image_url,
                caption=f"🎨 <b>Название:</b> {title}\n(<i>перевод</i>: {translated_title})\n👨‍🎨 <b>Автор:</b> {creator}",
                parse_mode="HTML"
            )

    
    @bot.message_handler(commands=['chicagogallery'])
    def get_painting_museum_chicago_random(message): 
        '''API коллекция Чикагского института искусств'''
        chat = message.chat
        bot.send_message(chat_id=chat.id, 
                             text=f"@{chat.username}, подождите, мы загружаем произведения искусства...")
        
        random_page = random.randint(1, 1000)
        
        response = requests.get(
            "https://api.artic.edu/api/v1/artworks/search",
            params={
                "query[term][is_public_domain]": "true",
                "limit": 1,
                "fields": "id,title,artist_title,image_id",
                "page": random_page, 
            }
        )
        response.raise_for_status()
        
        data = response.json()
        
        if data["data"]:
            artwork = data["data"][0]
            image_url = f"https://www.artic.edu/iiif/2/{artwork['image_id']}/full/843,/0/default.jpg"
            
            translated_title = TextTranslator.translate_to_russian(artwork['title'])
            
            bot.send_photo(
                chat.id,
                photo=image_url,
                caption=f"🎨 <b>Название:</b> {artwork['title']}\n(<i>перевод</i>: {translated_title})\n👨‍🎨 <b>Автор:</b> {artwork.get('artist_title', 'Неизвестен')}",
                parse_mode="HTML"
            )