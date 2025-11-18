import json
import os
from config import TEXT_POSITION
from text_renderer import create_text_block
from video_generator import create_video_from_data
from utils import get_temp_path, setup_directories

def load_json_data(filename):
    """Загружает данные из JSON файла"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def main(output_path=None):
    print("=== Thai Video Generator ===")
    print("Загружаем данные...")
    data = load_json_data('input.json')
    
    print(f"Загружено {len(data)} слов")
    print("Конфигурация загружена:")
    print(f"  Размер экрана: {TEXT_POSITION['screen']['width']}x{TEXT_POSITION['screen']['height']}")
    
    # Настраиваем директории в Downloads
    setup_directories()
    
    # Тестируем text_renderer
    print("\n🔤 Тестируем модуль text_renderer...")
    test_image = create_text_block(data[0])
    test_image_path = get_temp_path('frame_cache', 'test_block.png')
    test_image.save(test_image_path)
    print(f"✅ Тестовый блок сохранен: {test_image_path}")
    
    # Если путь не указан, используем временный в Downloads
    if output_path is None:
        output_path = get_temp_path("temp_video.mp4")
    
    # Создаем финальное видео с аудио
    print("\n🎬 Создаем финальное видео с аудио...")
    create_video_from_data(data, output_path)
    
    print("\n🎉 Стандартный режим завершен!")

if __name__ == "__main__":
    main()