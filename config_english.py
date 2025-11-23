import os

# Базовые пути
USER_HOME = os.path.expanduser("~")
DOWNLOADS_PATH = os.path.join(USER_HOME, "Downloads")
APP_TEMP_PATH = os.path.join(DOWNLOADS_PATH, "english_video_temp")

# Конфигурация позиционирования текста для английского
TEXT_POSITION = {
    'screen': {
        'width': 1080,
        'height': 1920
    },
    'fonts': {
        'english_size': 120,     # Крупный шрифт для английского
        'russian_size': 48       # Шрифт для русского перевода
    },
    'positions': {
        # Позиции для двух строк: русский и английский
        'russian_y': 709,        # Позиция русского текста
        'english_y': 860         # Позиция английского текста (центрирован)
    },
    'colors': {
        'background': 'white',
        'english': 'black',      # Английский текст - черный
        'russian': 'gray'        # Русский перевод - серый
    }
}