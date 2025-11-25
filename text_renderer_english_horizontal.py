from PIL import Image, ImageDraw, ImageFont
from config_english_horizontal import TEXT_POSITION
from text_utils import wrap_text

def create_english_horizontal_text_block(data):
    """Создает изображение текстового блока для горизонтального английского видео с переносом строк"""
    width = TEXT_POSITION['screen']['width']
    height = TEXT_POSITION['screen']['height']
    
    # Создаем белое изображение (горизонтальный формат)
    img = Image.new('RGB', (width, height), color=TEXT_POSITION['colors']['background'])
    draw = ImageDraw.Draw(img)
    
    try:
        # Шрифты для английского и русского
        english_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", TEXT_POSITION['fonts']['english_size'])
        russian_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", TEXT_POSITION['fonts']['russian_size'])
        
    except Exception as e:
        print(f"Ошибка загрузки шрифтов: {e}")
        print("Используем стандартные шрифты...")
        english_font = ImageFont.load_default()
        russian_font = ImageFont.load_default()
    
    # Центральные координаты
    center_x = width // 2
    
    # Русский перевод (сверху)
    russian_bbox = draw.textbbox((0, 0), data['russian'], font=russian_font)
    russian_width = russian_bbox[2] - russian_bbox[0]
    russian_x = center_x - russian_width // 2
    russian_y = TEXT_POSITION['positions']['russian_y']
    
    draw.text((russian_x, russian_y), data['russian'], 
              fill=TEXT_POSITION['colors']['russian'], font=russian_font)
    
    # Английский текст с переносом строк
    english_lines = wrap_text(data['english'])
    
    # Фиксированная позиция для первой строки английского текста
    first_line_y = TEXT_POSITION['positions']['english_y']
    line_height = english_font.size + 10  # Высота строки + отступ
    
    # Рисуем каждую строку английского текста
    for i, line in enumerate(english_lines):
        english_bbox = draw.textbbox((0, 0), line, font=english_font)
        english_width = english_bbox[2] - english_bbox[0]
        english_x = center_x - english_width // 2
        english_y = first_line_y + (i * line_height)  # Каждая следующая строка ниже предыдущей
        
        draw.text((english_x, english_y), line, 
                  fill=TEXT_POSITION['colors']['english'], font=english_font)
    
    return img