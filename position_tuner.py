import json
import os
from text_renderer import create_text_block
from config import TEXT_POSITION
from utils import get_temp_path, setup_directories

def load_test_data():
    """Загружает тестовые данные"""
    with open('input.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def test_russian_position():
    """Тестирует разные позиции для русского текста от 600 до 709"""
    data = load_test_data()
    test_word = data[0]
    
    # Настраиваем директории в Downloads
    setup_directories()
    
    # Фиксируем тайский и транслит на текущих позициях
    thai_y = 760
    translit_y = 960
    
    # Диапазон позиций для русского текста: от 600 до 709
    # Включаем ключевые позиции и 709
    russian_y_values = [600, 620, 640, 650, 660, 670, 680, 690, 700, 709]
    
    print("Тестируем позиции для русского текста от 600 до 709")
    print(f"Тайский фиксирован на Y={thai_y}")
    print(f"Транслит фиксирован на Y={translit_y}")
    print(f"Текущая позиция русского: 709")
    print(f"Будет создано {len(russian_y_values)} изображений")
    
    for russian_y in russian_y_values:
        # Временно изменяем конфигурацию
        original_russian_y = TEXT_POSITION['positions']['russian_y']
        TEXT_POSITION['positions']['russian_y'] = russian_y
        TEXT_POSITION['positions']['thai_y'] = thai_y
        TEXT_POSITION['positions']['translit_y'] = translit_y
        
        # Создаем изображение
        image = create_text_block(test_word)
        
        # Сохраняем в Downloads
        filename = get_temp_path('frame_cache', f'test_russian_y_{russian_y}.png')
        image.save(filename)
        print(f"Создано: {filename}")
        
        # Восстанавливаем значение
        TEXT_POSITION['positions']['russian_y'] = original_russian_y
    
    print("\nТестирование завершено!")
    print("Открывайте изображения для сравнения:")
    for russian_y in [650, 660, 670, 680, 690, 700, 709]:
        filepath = get_temp_path('frame_cache', f'test_russian_y_{russian_y}.png')
        print(f"open {filepath}")

if __name__ == "__main__":
    test_russian_position()