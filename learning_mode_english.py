import os
import cv2
import numpy as np
from PIL import Image
import subprocess
from text_renderer_english import create_english_text_block
from config_english import TEXT_POSITION, APP_TEMP_PATH

class EnglishLearningAudioGenerator:
    def __init__(self):
        self.temp_dir = os.path.join(APP_TEMP_PATH, 'audio_files')
        os.makedirs(self.temp_dir, exist_ok=True)
        
    def generate_learning_audio(self, text, filename):
        """Генерирует аудио файл с английским произношением + тишина для повторения"""
        try:
            from gtts import gTTS
            
            # Генерируем основное аудио
            tts = gTTS(text=text, lang='en')  # Английский язык
            main_audio_path = os.path.join(self.temp_dir, f"main_{filename}")
            tts.save(main_audio_path)
            
            # Получаем длительность основного аудио
            main_duration = self.get_audio_duration(main_audio_path)
            
            # Создаем файл тишины такой же длительности
            silence_path = os.path.join(self.temp_dir, f"silence_{filename}")
            self.create_silence_audio(main_duration, silence_path)
            
            # Объединяем основное аудио и тишину
            final_audio_path = os.path.join(self.temp_dir, filename)
            self.concat_audio_files([main_audio_path, silence_path], final_audio_path)
            
            # Удаляем временные файлы
            if os.path.exists(main_audio_path):
                os.remove(main_audio_path)
            if os.path.exists(silence_path):
                os.remove(silence_path)
            
            final_duration = self.get_audio_duration(final_audio_path)
            print(f"Аудио создано: {filename} (длительность: {final_duration:.2f}с = {main_duration:.2f}с + {main_duration:.2f}с тишины)")
            
            return final_audio_path, final_duration
            
        except Exception as e:
            print(f"Ошибка генерации аудио для '{text}': {e}")
            return None, 0
    
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
    
    def create_silence_audio(self, duration, output_path):
        """Создает аудио файл тишины заданной длительности"""
        subprocess.run([
            'ffmpeg', '-f', 'lavfi', '-i', f'anullsrc=channel_layout=stereo:sample_rate=44100',
            '-t', str(duration), output_path, '-y'
        ], check=True, capture_output=True)
    
    def concat_audio_files(self, audio_files, output_path):
        """Объединяет аудио файлы"""
        concat_list = os.path.join(APP_TEMP_PATH, "english_audio_concat_list.txt")
        with open(concat_list, 'w') as f:
            for audio_file in audio_files:
                abs_path = os.path.abspath(audio_file)
                f.write(f"file '{abs_path}'\n")
        
        try:
            subprocess.run([
                'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list,
                '-c', 'copy', output_path, '-y'
            ], check=True, capture_output=True)
        finally:
            if os.path.exists(concat_list):
                os.remove(concat_list)

class EnglishLearningVideoGenerator:
    def __init__(self):
        self.width = TEXT_POSITION['screen']['width']
        self.height = TEXT_POSITION['screen']['height']
        self.fps = 24
        
    def create_learning_video(self, word_data, audio_duration, output_path):
        """Создает видео для одного английского слова с точной длительностью под аудио"""
        print(f"Создаем видео для слова: {word_data['english']} (длительность: {audio_duration:.2f}с)")
        
        # Создаем VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Создаем изображение для слова
        pil_image = create_english_text_block(word_data)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Добавляем кадры на точную длительность аудио
        frames_count = int(audio_duration * self.fps)
        for _ in range(frames_count):
            video_writer.write(opencv_image)
        
        video_writer.release()
        
        return output_path

class EnglishLearningHorizontalVideoGenerator:
    def __init__(self):
        from config_english_horizontal import TEXT_POSITION
        self.width = TEXT_POSITION['screen']['width']
        self.height = TEXT_POSITION['screen']['height']
        self.fps = 24
        
    def create_learning_video(self, word_data, audio_duration, output_path):
        """Создает горизонтальное видео для одного английского слова с точной длительностью под аудио"""
        from text_renderer_english_horizontal import create_english_horizontal_text_block
        
        print(f"Создаем горизонтальное видео для слова: {word_data['english']} (длительность: {audio_duration:.2f}с)")
        
        # Создаем VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Создаем изображение для слова
        pil_image = create_english_horizontal_text_block(word_data)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Добавляем кадры на точную длительность аудио
        frames_count = int(audio_duration * self.fps)
        for _ in range(frames_count):
            video_writer.write(opencv_image)
        
        video_writer.release()
        
        return output_path

def generate_english_horizontal_learning_video(words_data, output_path):
    """Основная функция для создания горизонтального видео в режиме заучивания английского"""
    print("🎓 РЕЖИМ ЗАУЧИВАНИЯ АНГЛИЙСКОГО (ГОРИЗОНТАЛЬНОЕ)")
    print("="*50)
    
    # Создаем папки
    os.makedirs(os.path.join(APP_TEMP_PATH, 'audio_files'), exist_ok=True)
    
    # Генерируем аудио для каждого слова
    audio_generator = EnglishLearningAudioGenerator()
    video_generator = EnglishLearningHorizontalVideoGenerator()
    
    word_videos = []
    audio_durations = []
    
    print("\n🔊 Генерируем аудио файлы...")
    for i, word in enumerate(words_data):
        audio_file, audio_duration = audio_generator.generate_learning_audio(
            word['english'], f"english_horizontal_learning_word_{i+1}.mp3"
        )
        if audio_file and audio_duration > 0:
            audio_durations.append(audio_duration)
        else:
            audio_durations.append(2.0)
    
    print("\n🎬 Создаем горизонтальное видео для каждого слова...")
    for i, (word, duration) in enumerate(zip(words_data, audio_durations)):
        word_video_path = os.path.join(APP_TEMP_PATH, f"english_horizontal_learning_word_{i+1}.mp4")
        video_path = video_generator.create_learning_video(word, duration, word_video_path)
        
        # Добавляем аудио к видео
        final_word_video = video_path.replace('.mp4', '_with_audio.mp4')
        audio_file = os.path.join(APP_TEMP_PATH, 'audio_files', f"english_horizontal_learning_word_{i+1}.mp3")
        
        if os.path.exists(audio_file):
            subprocess.run([
                'ffmpeg', '-i', video_path, '-i', audio_file,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                final_word_video, '-y'
            ], check=True)
            word_videos.append(final_word_video)
        else:
            print(f"⚠️ Аудио файл не найден: {audio_file}")
    
    # Объединяем все видео в одно
    print("\n🔗 Объединяем горизонтальные видео...")
    concat_list_file = os.path.join(APP_TEMP_PATH, "english_horizontal_learning_concat_list.txt")
    
    with open(concat_list_file, 'w') as f:
        for video_file in word_videos:
            if video_file and os.path.exists(video_file):
                abs_path = os.path.abspath(video_file)
                f.write(f"file '{abs_path}'\n")
    
    # Проверяем, есть ли файлы для объединения
    if os.path.exists(concat_list_file):
        with open(concat_list_file, 'r') as f:
            content = f.read().strip()
            if not content:
                print("❌ Нет видео файлов для объединения")
                return None
        
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_file,
            '-c', 'copy', output_path, '-y'
        ], check=True)
        
        print(f"✅ Горизонтальное видео в режиме заучивания английского создано: {output_path}")
        
        total_duration = sum(audio_durations)
        print(f"📊 Общая длительность: {total_duration:.2f} секунд")
        return output_path
    else:
        print("❌ Не удалось создать список для объединения видео")
        return None

def generate_english_learning_video(words_data, output_path):
    """Основная функция для создания видео в режиме заучивания английского"""
    print("🎓 РЕЖИМ ЗАУЧИВАНИЯ АНГЛИЙСКОГО")
    print("="*50)
    
    # Создаем папки
    os.makedirs(os.path.join(APP_TEMP_PATH, 'audio_files'), exist_ok=True)
    
    # Генерируем аудио для каждого слова
    audio_generator = EnglishLearningAudioGenerator()
    video_generator = EnglishLearningVideoGenerator()
    
    word_videos = []
    audio_durations = []
    
    print("\n🔊 Генерируем аудио файлы...")
    for i, word in enumerate(words_data):
        audio_file, audio_duration = audio_generator.generate_learning_audio(
            word['english'], f"english_learning_word_{i+1}.mp3"
        )
        if audio_file and audio_duration > 0:
            audio_durations.append(audio_duration)
        else:
            audio_durations.append(2.0)
    
    print("\n🎬 Создаем видео для каждого слова...")
    for i, (word, duration) in enumerate(zip(words_data, audio_durations)):
        word_video_path = os.path.join(APP_TEMP_PATH, f"english_learning_word_{i+1}.mp4")
        video_path = video_generator.create_learning_video(word, duration, word_video_path)
        
        # Добавляем аудио к видео
        final_word_video = video_path.replace('.mp4', '_with_audio.mp4')
        audio_file = os.path.join(APP_TEMP_PATH, 'audio_files', f"english_learning_word_{i+1}.mp3")
        
        if os.path.exists(audio_file):
            subprocess.run([
                'ffmpeg', '-i', video_path, '-i', audio_file,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                final_word_video, '-y'
            ], check=True)
            word_videos.append(final_word_video)
        else:
            print(f"⚠️ Аудио файл не найден: {audio_file}")
    
    # Объединяем все видео в одно
    print("\n🔗 Объединяем видео...")
    concat_list_file = os.path.join(APP_TEMP_PATH, "english_learning_concat_list.txt")
    
    with open(concat_list_file, 'w') as f:
        for video_file in word_videos:
            if video_file and os.path.exists(video_file):
                abs_path = os.path.abspath(video_file)
                f.write(f"file '{abs_path}'\n")
    
    # Проверяем, есть ли файлы для объединения
    if os.path.exists(concat_list_file):
        with open(concat_list_file, 'r') as f:
            content = f.read().strip()
            if not content:
                print("❌ Нет видео файлов для объединения")
                return None
        
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_file,
            '-c', 'copy', output_path, '-y'
        ], check=True)
        
        print(f"✅ Видео в режиме заучивания английского создано: {output_path}")
        
        total_duration = sum(audio_durations)
        print(f"📊 Общая длительность: {total_duration:.2f} секунд")
        return output_path
    else:
        print("❌ Не удалось создать список для объединения видео")
        return None