from telebot import TeleBot
from bot.services.logger import setup_logger
from media_resource.answers import *

logger = setup_logger(__name__)


def setup_text_handlers(bot: TeleBot):
    @bot.message_handler(content_types=['text'])
    def get_text_answer(message):
        '''Ответ на текстовые сообщения'''
        chat = message.chat
        text_user = message.text.lower()
        
        if any(word in text_user for word in hello_words):
            bot.send_sticker(
                chat_id=chat.id, 
                sticker='CAACAgIAAxkBAAEQbjdoa4S2gUYeDKgXHBVgJk-nytfVvgACqTAAAtl6YUhFJ3U8c3TZSjYE'
                )
            return
        
        if any(word in text_user for word in bye_words):
            bot.send_message(
                chat_id=chat.id, 
                text=f'{chat.username}, может еще увидимся...'
            )
            bot.send_sticker(
                chat_id=chat.id, 
                sticker='CAACAgIAAxkBAAEQejdobUMsdk-ddyS0Gb8MC52MBI04VAACOSIAArVQGUjex_gbjRrQ5jYE'
                )
            return 
            
            
        bot.send_message(
            chat_id=chat.id, 
            text=f'{chat.username}, я еще плохо умею говорить. Лучше попробуйте команды, написав /help\n\nВот гифка для настроения:'
            )

        bot.send_animation(
            chat_id=chat.id,
            animation="CgACAgIAAxkBAAPEaGofAV4_5AiDzHBdDWLhWS6oNa8AAvoOAAKVy0FImcdV64Q0oK82BA"
        )
