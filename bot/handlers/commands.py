from telebot import TeleBot, types
from ..keyboards import add_main_keyboard, start_keyboard, add_quote, add_gallery, add_courses_rates


def setup_commands_handlers(bot: TeleBot):
    @bot.message_handler(commands=['help'])
    def get_help_bot(message):
        '''Обработчик команды help'''
        chat = message.chat
        
        help_text = (
        "<b>Основные команды:</b>\n"
        "/start - Начать работу с ботом\n"
        "/help - Получить справку по командам\n\n"
        "<b>📚 Функционал бота:</b>\n"
        "/numfact - Случайный факт о числах\n"
        "/today - 10 исторических событий прошлого, которые произошли в этот день\n"
        "/holiday - Возможность узнать случайный праздник сегодня\n"
        "/quote - Сборники цитат на разные темы\n"
        "/museum - Коллекции экспозиций разный музеев и галерей\n"
        "/rates - Котировки валют(и криптовалют), металлов и нефти\n"
        "/weather_info - Получение данных о погоде\n\n"
        "<i>Применяйте функции, используя меню бота. Приятного пользования!</i>"
        )

        bot.send_message(
            chat_id=chat.id, 
            text=help_text, 
            reply_markup=add_main_keyboard(),
            parse_mode="HTML"
        )
    
    @bot.message_handler(commands=['start'])
    def get_start_bot(message):
        '''Обработчик команды start'''
        chat = message.chat
        start_text = (
        f"<b>👋 Привет, {message.from_user.first_name}!</b>\n\n"
        "Я - многофункциональный бот с широкими возможностями:\n"
        "🎨 <i>Искусство и культура</i>\n"
        "📚 <i>Образовательные материалы</i>\n"
        "✨ <i>Развлекательный контент</i>\n"
        "🛠 <i>Полезные инструменты</i>\n\n"
        "<b>Нажмите /help</b>, чтобы увидеть все мои возможности или\n"
        "используйте подсказки в меню ниже."
        )
        bot.send_message(
            chat_id=chat.id, 
            text=start_text, 
            reply_markup=start_keyboard(),
            parse_mode="HTML"
        )
        
    @bot.message_handler(commands=['quote'])
    def get_quote_bot(message):
        '''Обработчик команды quote'''
        chat = message.chat
        bot.send_message(
            chat_id=chat.id, 
            text='Выбирайте команду и получайте цитату связанную с темой.', 
            reply_markup=add_quote(),
        )
        
    @bot.message_handler(commands=['museum'])
    def get_museum_bot(message):
        '''Обработчик команды museum'''
        chat = message.chat
        bot.send_message(
            chat_id=chat.id, 
            text='Выбирайте команду и смотрите картины со всего мира!', 
            reply_markup=add_gallery(),
        )
        
    @bot.message_handler(commands=['rates'])
    def get_rates_bot(message):
        '''Обработчик команды rates'''
        chat = message.chat
        bot.send_message(
            chat_id=chat.id, 
            text='Выбирайте команду и смотрите котировки металлов, валют и нефти', 
            reply_markup=add_courses_rates(),
        )
