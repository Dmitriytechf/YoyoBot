from googletrans import Translator
from bot.services.logger import setup_logger

logger = setup_logger(__name__)

class TextTranslator:
    @staticmethod
    def translate_to_russian(text: str) -> str:
        try:
            translator = Translator()
            return translator.translate(text, src='en', dest='ru').text
        except Exception as e:
            logger.error(f'Ошибка перевода: {e}')
            return text
            