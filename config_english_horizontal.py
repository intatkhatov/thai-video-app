import os

# Базовые пути
USER_HOME = os.path.expanduser("~")
DOWNLOADS_PATH = os.path.join(USER_HOME, "Downloads")
APP_TEMP_PATH = os.path.join(DOWNLOADS_PATH, "english_horizontal_video_temp")

# Конфигурация позиционирования текста для горизонтального английского
TEXT_POSITION = {
    'screen': {
        'width': 1920,    # Горизонтальное видео
        'height': 1080    # Шире чем высота
    },
    'fonts': {
        'english_size': 100,     # Немного меньше для горизонтального
        'russian_size': 42       # Шрифт для русского перевода
    },
    'positions': {
        # Позиции для двух строк в горизонтальном формате
        'russian_y': 400,        # Позиция русского текста
        'english_y': 600         # Позиция английского текста
    },
    'colors': {
        'background': 'white',
        'english': 'black',
        'russian': 'gray'
    }
}