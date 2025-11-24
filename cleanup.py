import os
import shutil
from config import APP_TEMP_PATH as THAI_TEMP_PATH
from config_english import APP_TEMP_PATH as ENGLISH_TEMP_PATH
from config_english_horizontal import APP_TEMP_PATH as ENGLISH_HORIZONTAL_TEMP_PATH

def cleanup_temp_files():
    """Удаляет временные файлы и папки для всех языков и ориентаций"""
    temp_folders = [
        THAI_TEMP_PATH,
        os.path.join(THAI_TEMP_PATH, 'audio_files'),
        os.path.join(THAI_TEMP_PATH, 'frame_cache'),
        ENGLISH_TEMP_PATH,
        os.path.join(ENGLISH_TEMP_PATH, 'audio_files'),
        os.path.join(ENGLISH_TEMP_PATH, 'frame_cache'),
        ENGLISH_HORIZONTAL_TEMP_PATH,
        os.path.join(ENGLISH_HORIZONTAL_TEMP_PATH, 'audio_files'),
        os.path.join(ENGLISH_HORIZONTAL_TEMP_PATH, 'frame_cache')
    ]
    
    print("\n🧹 Очищаем временные файлы...")
    
    deleted_count = 0
    for folder in temp_folders:
        if os.path.exists(folder):
            try:
                # Считаем количество файлов перед удалением
                file_count = sum(len(files) for _, _, files in os.walk(folder))
                shutil.rmtree(folder)
                print(f"✅ Удалено: {folder} ({file_count} файлов)")
                deleted_count += file_count
            except Exception as e:
                print(f"⚠️ Не удалось удалить {folder}: {e}")
    
    # Проверяем, остались ли отдельные временные файлы
    temp_files = [
        os.path.join(THAI_TEMP_PATH, 'audio_list.txt'),
        os.path.join(THAI_TEMP_PATH, 'concat_list.txt'),
        os.path.join(THAI_TEMP_PATH, 'combined_audio.mp3'),
        os.path.join(THAI_TEMP_PATH, 'audio_concat_list.txt'),
        os.path.join(THAI_TEMP_PATH, 'learning_concat_list.txt'),
        os.path.join(ENGLISH_TEMP_PATH, 'english_concat_list.txt'),
        os.path.join(ENGLISH_TEMP_PATH, 'english_audio_concat_list.txt'),
        os.path.join(ENGLISH_TEMP_PATH, 'english_learning_concat_list.txt'),
        os.path.join(ENGLISH_HORIZONTAL_TEMP_PATH, 'english_horizontal_concat_list.txt'),
        os.path.join(ENGLISH_HORIZONTAL_TEMP_PATH, 'english_horizontal_learning_concat_list.txt')
    ]
    
    for file in temp_files:
        if os.path.exists(file):
            try:
                os.remove(file)
                print(f"✅ Удалено: {file}")
                deleted_count += 1
            except Exception as e:
                print(f"⚠️ Не удалось удалить {file}: {e}")
    
    print(f"🎉 Очистка завершена! Удалено файлов: {deleted_count}")

def keep_temp_files():
    """Сохраняет временные файлы для отладки"""
    print(f"\n📁 Временные файлы сохранены:")
    print(f"   - {THAI_TEMP_PATH}/ - тайский язык")
    print(f"   - {ENGLISH_TEMP_PATH}/ - английский (вертикальное)")
    print(f"   - {ENGLISH_HORIZONTAL_TEMP_PATH}/ - английский (горизонтальное)")
    print("💡 Вы можете просмотреть аудио файлы и тестовые изображения")

def ask_for_cleanup():
    """Спрашивает пользователя о очистке временных файлов"""
    print("\n" + "="*50)
    print("🧹 УДАЛЕНИЕ ВРЕМЕННЫХ ФАЙЛОВ")
    print("="*50)
    
    while True:
        response = input("Очистить временные файлы? (y/n): ").strip().lower()
        if response in ['y', 'yes', 'д', 'да']:
            cleanup_temp_files()
            break
        elif response in ['n', 'no', 'н', 'нет']:
            keep_temp_files()
            break
        else:
            print("❌ Пожалуйста, введите 'y' (да) или 'n' (нет)")

if __name__ == "__main__":
    cleanup_temp_files()