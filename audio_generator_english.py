import os
from gtts import gTTS
import subprocess
from config_english import APP_TEMP_PATH

class EnglishAudioGenerator:
    def __init__(self):
        self.temp_dir = os.path.join(APP_TEMP_PATH, 'audio_files')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def generate_audio(self, text, filename):
        """Генерирует аудио файл с английским произношением"""
        try:
            tts = gTTS(text=text, lang='en')  # Английский язык
            filepath = os.path.join(self.temp_dir, filename)
            tts.save(filepath)
            print(f"Аудио создано: {filepath}")
            return filepath
        except Exception as e:
            print(f"Ошибка генерации аудио для '{text}': {e}")
            return None
    
    def get_audio_duration(self, audio_file):
        """Получает длительность аудио файла"""
        try:
            result = subprocess.run([
                'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1', audio_file
            ], capture_output=True, text=True)
            return float(result.stdout.strip())
        except:
            return 1.0

def generate_english_audio_for_words(words_data):
    """Генерирует аудио файлы для всех английских слов"""
    generator = EnglishAudioGenerator()
    audio_files = []
    
    for i, word in enumerate(words_data):
        audio_file = generator.generate_audio(word['english'], f"english_word_{i+1}.mp3")
        if audio_file:
            duration = generator.get_audio_duration(audio_file)
            audio_files.append({
                'file': audio_file,
                'word': word,
                'duration': duration
            })
            print(f"Длительность аудио: {duration:.2f} секунд")
    
    return audio_files