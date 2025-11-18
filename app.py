import json
import os
from main import main as standard_main
from learning_mode import generate_learning_video
from cleanup import ask_for_cleanup
from utils import setup_directories
from config import DOWNLOADS_PATH

def load_json_data(filename):
    """Загружает данные из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def select_mode():
    """Выбор режима работы приложения"""
    print("="*50)
    print("🎬 ГЕНЕРАТОР ВИДЕО ДЛЯ ИЗУЧЕНИЯ ТАЙСКОГО")
    print("="*50)
    print("Выберите режим работы приложения:")
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

def get_downloads_path(mode):
    """Возвращает путь для сохранения видео в Downloads"""
    if mode == 'standard':
        return os.path.join(DOWNLOADS_PATH, "thai_standard_video.mp4")
    else:
        return os.path.join(DOWNLOADS_PATH, "thai_learning_video.mp4")

def main():
    # Настраиваем директории в Downloads
    setup_directories()
    
    # Загружаем данные
    data = load_json_data('input.json')
    print(f"📝 Загружено слов: {len(data)}")
    
    # Выбираем режим
    mode = select_mode()
    
    # Получаем путь для сохранения в Downloads
    downloads_output = get_downloads_path(mode)
    
    # Запускаем выбранный режим
    if mode == 'standard':
        print("\n🚀 Запускаем СТАНДАРТНЫЙ режим...")
        standard_main(downloads_output)
        print(f"✅ Видео сохранено в: {downloads_output}")
            
    else:
        print("\n🚀 Запускаем режим ЗАУЧИВАНИЯ...")
        generate_learning_video(data, downloads_output)
        print(f"✅ Видео сохранено в: {downloads_output}")
    
    # Спрашиваем о очистке в обоих режимах
    ask_for_cleanup()
    
    print("\n🎉 Работа приложения завершена!")

if __name__ == "__main__":
    main()