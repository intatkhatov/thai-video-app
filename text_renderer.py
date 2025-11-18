from PIL import Image, ImageDraw, ImageFont
from config import TEXT_POSITION

def create_text_block(data):
    """Создает изображение текстового блока в стиле iOS"""
    width = TEXT_POSITION['screen']['width']
    height = TEXT_POSITION['screen']['height']
    
    # Создаем белое изображение (вертикальный формат iPhone 14 Pro)
    img = Image.new('RGB', (width, height), color=TEXT_POSITION['colors']['background'])
    draw = ImageDraw.Draw(img)
    
    try:
        # Специальные шрифты для тайского языка в macOS
        thai_fonts = [
            "/System/Library/Fonts/Thonburi.ttc",           # Основной тайский шрифт
            "/System/Library/Fonts/AppleGothic.ttc",        # Альтернативный
            "/System/Library/Fonts/Arial.ttf",              # Arial поддерживает тайский
            "/System/Library/Fonts/Helvetica.ttc",          # Helvetica
        ]
        
        thai_font = None
        for font_path in thai_fonts:
            try:
                thai_font = ImageFont.truetype(font_path, TEXT_POSITION['fonts']['thai_size'])
                # Проверяем, поддерживает ли шрифт тайские символы
                test_bbox = draw.textbbox((0, 0), data['thai'], font=thai_font)
                print(f"Успешно загружен шрифт для тайского: {font_path}")
                break
            except Exception as e:
                print(f"Шрифт {font_path} не подошел: {e}")
                continue
        
        if thai_font is None:
            raise Exception("Не найден подходящий шрифт для тайского языка")
        
        # Шрифты для русского и транслитерации
        translit_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", TEXT_POSITION['fonts']['translit_size'])
        russian_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", TEXT_POSITION['fonts']['russian_size'])
        
    except Exception as e:
        print(f"Ошибка загрузки шрифтов: {e}")
        print("Пробуем использовать стандартные шрифты...")
        # Используем стандартные шрифты в случае ошибки
        thai_font = ImageFont.load_default()
        translit_font = ImageFont.load_default()
        russian_font = ImageFont.load_default()
    
    # Абсолютные позиции из конфигурации
    positions = {
        'russian': {
            'x': width // 2,
            'y': TEXT_POSITION['positions']['russian_y']
        },
        'thai': {
            'x': width // 2,
            'y': TEXT_POSITION['positions']['thai_y']
        },
        'translit': {
            'x': width // 2,
            'y': TEXT_POSITION['positions']['translit_y']
        }
    }
    
    # Рисуем текст
    _draw_text_elements(draw, data, positions, thai_font, russian_font, translit_font)
    
    return img

def _draw_text_elements(draw, data, positions, thai_font, russian_font, translit_font):
    """Рисует все текстовые элементы на изображении"""
    # Русский текст (центрируем)
    russian_bbox = draw.textbbox((0, 0), data['russian'], font=russian_font)
    russian_width = russian_bbox[2] - russian_bbox[0]
    russian_x = positions['russian']['x'] - russian_width // 2
    draw.text((russian_x, positions['russian']['y']), data['russian'], 
              fill=TEXT_POSITION['colors']['russian'], font=russian_font)
    
    # Тайский текст (центрируем)
    thai_bbox = draw.textbbox((0, 0), data['thai'], font=thai_font)
    thai_width = thai_bbox[2] - thai_bbox[0]
    thai_x = positions['thai']['x'] - thai_width // 2
    draw.text((thai_x, positions['thai']['y']), data['thai'], 
              fill=TEXT_POSITION['colors']['thai'], font=thai_font)
    
    # Транслитерация (центрируем)
    translit_bbox = draw.textbbox((0, 0), data['transliteration'], font=translit_font)
    translit_width = translit_bbox[2] - translit_bbox[0]
    translit_x = positions['translit']['x'] - translit_width // 2
    draw.text((translit_x, positions['translit']['y']), data['transliteration'], 
              fill=TEXT_POSITION['colors']['translit'], font=translit_font)