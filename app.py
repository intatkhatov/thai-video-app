import json
import os
from main import main as standard_main_thai
from learning_mode import generate_learning_video as generate_learning_thai
from learning_mode_english import generate_english_learning_video
from video_generator_english import create_english_video_from_data
from cleanup import ask_for_cleanup
from utils import setup_directories
from config_english import DOWNLOADS_PATH

def load_json_data(filename):
    """Загружает данные из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def select_language():
    """Выбор языка обучения"""
    print("="*50)
    print("🎬 ГЕНЕРАТОР ВИДЕО ДЛЯ ИЗУЧЕНИЯ ЯЗЫКОВ")
    print("="*50)
    print("Выберите язык для изучения:")
    print("1. 🇹🇭 Тайский")
    print("2. 🇬🇧 Английский")
    print("="*50)
    
    while True:
        choice = input("Введите номер языка (1 или 2): ").strip()
        if choice == '1':
            return 'thai'
        elif choice == '2':
            return 'english'
        else:
            print("❌ Пожалуйста, введите 1 или 2")

def select_mode(language):
    """Выбор режима работы приложения"""
    print(f"\n📝 Выбран язык: {'Тайский' if language == 'thai' else 'Английский'}")
    print("="*50)
    print("Выберите режим работы:")
    print("1. 📺 Стандартный")
    print("   - Каждое слово показывается 3 секунды")
    print("   - Произношение звучит один раз")
    print("2. 🎓 Заучивание") 
    print("   - Длительность адаптируется под произношение")
    print("   - После произношения - пауза для повторения")
    print("="*50)
    
    while True:
        choice = input("Введите номер режима (1 или 2): ").strip()
        if choice == '1':
            return 'standard'
        elif choice == '2':
            return 'learning'
        else:
            print("❌ Пожалуйста, введите 1 или 2")

def get_downloads_path(language, mode):
    """Возвращает путь для сохранения видео в Downloads"""
    if language == 'thai':
        if mode == 'standard':
            return os.path.join(DOWNLOADS_PATH, "thai_standard_video.mp4")
        else:
            return os.path.join(DOWNLOADS_PATH, "thai_learning_video.mp4")
    else:  # english
        if mode == 'standard':
            return os.path.join(DOWNLOADS_PATH, "english_standard_video.mp4")
        else:
            return os.path.join(DOWNLOADS_PATH, "english_learning_video.mp4")

def main():
    # Настраиваем директории
    setup_directories()
    
    # Выбираем язык
    language = select_language()
    
    # Загружаем данные
    if language == 'thai':
        data = load_json_data('input.json')
    else:
        data = load_json_data('input_english.json')
    
    print(f"📝 Загружено слов: {len(data)}")
    
    # Выбираем режим
    mode = select_mode(language)
    
    # Получаем путь для сохранения в Downloads
    downloads_output = get_downloads_path(language, mode)
    
    # Запускаем выбранный режим и язык
    if language == 'thai':
        if mode == 'standard':
            print("\n🚀 Запускаем СТАНДАРТНЫЙ режим для тайского...")
            standard_main_thai(downloads_output)
        else:
            print("\n🚀 Запускаем режим ЗАУЧИВАНИЯ для тайского...")
            generate_learning_thai(data, downloads_output)
    else:  # english
        if mode == 'standard':
            print("\n🚀 Запускаем СТАНДАРТНЫЙ режим для английского...")
            create_english_video_from_data(data, downloads_output)
        else:
            print("\n🚀 Запускаем режим ЗАУЧИВАНИЯ для английского...")
            generate_english_learning_video(data, downloads_output)
    
    print(f"✅ Видео сохранено в: {downloads_output}")
    
    # Спрашиваем о очистке
    ask_for_cleanup()
    
    print("\n🎉 Работа приложения завершена!")

if __name__ == "__main__":
    main()