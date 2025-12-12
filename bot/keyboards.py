from telebot import types


def add_main_keyboard():
    '''Кнопки основных команд(в help)'''
    # Создание клавиатуры. Максимум две команды в строке
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Создание кнопок
    button_numfact = types.KeyboardButton('/numfact')
    button_today = types.KeyboardButton('/today')
    button_holidays = types.KeyboardButton('/holiday')
    button_quote = types.KeyboardButton('/quote')
    button_museum = types.KeyboardButton('/museum')
    button_rates = types.KeyboardButton('/rates')
    button_weather = types.KeyboardButton('/weather_info')
    
    keyboard.add(button_numfact, button_today, button_holidays, 
                 button_quote, button_museum, button_rates, button_weather)
    return keyboard


def add_quote():
    '''Отдельная функция для обработки цитат'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    button_randomquote = types.KeyboardButton('/randomquote')
    button_stoickquote = types.KeyboardButton('/stoickquote')
    button_lotrquote = types.KeyboardButton('/LOTRquote')
    

    keyboard.add(button_randomquote, button_stoickquote,button_lotrquote)
    return keyboard


def start_keyboard():
    '''Кнопки для команды start'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton('/help')
    keyboard.add(button_help)
    return keyboard


def add_gallery():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_gallery = types.KeyboardButton('/gallery')
    button_chicagogallery = types.KeyboardButton('/chicagogallery')
    
    keyboard.add(button_gallery, button_chicagogallery)
    return keyboard


def add_courses_rates():
    '''Отдельная функция для обработки различных котировок'''
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    button_valute = types.KeyboardButton('/valute')
    button_oil = types.KeyboardButton('/oil')
    button_crypto = types.KeyboardButton('/crypto')
    button_metals = types.KeyboardButton('/metals')
    
    keyboard.add(button_valute, button_oil, button_metals, button_crypto)
    return keyboard
