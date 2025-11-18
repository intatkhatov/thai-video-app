import os

# Базовые пути
USER_HOME = os.path.expanduser("~")
DOWNLOADS_PATH = os.path.join(USER_HOME, "Downloads")
APP_TEMP_PATH = os.path.join(DOWNLOADS_PATH, "thai_video_temp")

# Конфигурация позиционирования текста
TEXT_POSITION = {
    'screen': {
        'width': 1080,
        'height': 1920
    },
    'fonts': {
        'thai_size': 120,
        'russian_size': 48,
        'translit_size': 48
    },
    'positions': {
        # ФИНАЛЬНЫЕ ОПТИМАЛЬНЫЕ позиции Y для каждого элемента
        'russian_y': 709,        # ОПТИМАЛЬНАЯ позиция русского текста
        'thai_y': 760,           # ОПТИМАЛЬНАЯ позиция тайского текста
        'translit_y': 960        # ОПТИМАЛЬНАЯ позиция транслитерации
    },
    'colors': {
        'background': 'white',
        'thai': 'black',
        'russian': 'gray',
        'translit': 'gray'
    }
}