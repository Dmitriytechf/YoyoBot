from telebot import TeleBot
import random
from media_resource.stick import STICKER_IDS


def setup_stickers_handlers(bot: TeleBot):
    @bot.message_handler(content_types=['sticker'])
    def get_random_stick(message):
        '''Отправка случайных стикеров на стикер пользователя'''
        chat = message.chat
        random_sticker = random.choice(STICKER_IDS)
        
        bot.send_sticker(chat_id=chat.id, sticker=random_sticker)