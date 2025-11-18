import os
from config import APP_TEMP_PATH

def setup_directories():
    """Создает необходимые директории в Downloads"""
    directories = [
        APP_TEMP_PATH,
        os.path.join(APP_TEMP_PATH, 'audio_files'),
        os.path.join(APP_TEMP_PATH, 'frame_cache')
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    return APP_TEMP_PATH

def get_temp_path(*args):
    """Возвращает путь внутри временной папки"""
    return os.path.join(APP_TEMP_PATH, *args)