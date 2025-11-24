import os
import cv2
import numpy as np
from PIL import Image
import subprocess
from text_renderer_english import create_english_text_block
from config_english import TEXT_POSITION, APP_TEMP_PATH
from audio_generator_english import generate_english_audio_for_words

class EnglishVideoGenerator:
    def __init__(self):
        self.width = TEXT_POSITION['screen']['width']
        self.height = TEXT_POSITION['screen']['height']
        self.duration_per_word = 3  # 3 секунды на каждое слово
        self.fps = 24  # кадров в секунду
        
    def create_word_video_with_audio(self, word_data, audio_file, output_path):
        """Создает видео для одного английского слова с его аудио"""
        print(f"Создаем видео для слова: {word_data['english']}")
        
        # Создаем VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Создаем изображение для слова
        pil_image = create_english_text_block(word_data)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Добавляем кадры
        frames_count = self.duration_per_word * self.fps
        for _ in range(int(frames_count)):
            video_writer.write(opencv_image)
        
        video_writer.release()
        
        # Добавляем аудио к видео
        final_video_path = output_path.replace('.mp4', '_with_audio.mp4')
        subprocess.run([
            'ffmpeg', '-i', output_path, '-i', audio_file,
            '-c:v', 'copy', '-c:a', 'aac', '-shortest',
            final_video_path, '-y'
        ], check=True)
        
        return final_video_path
    
    def generate_video_with_audio(self, words_data, output_path):
        """Генерирует финальное видео с аудио для каждого английского слова"""
        print("Генерируем аудио файлы...")
        audio_files = generate_english_audio_for_words(words_data)
        
        # Создаем видео для каждого слова с его аудио
        word_videos = []
        for i, (word, audio_info) in enumerate(zip(words_data, audio_files)):
            word_video_path = os.path.join(APP_TEMP_PATH, f"english_word_{i+1}.mp4")
            final_word_video = self.create_word_video_with_audio(
                word, audio_info['file'], word_video_path
            )
            word_videos.append(final_word_video)
        
        # Объединяем все видео в одно
        self.concat_videos(word_videos, output_path)
        
        print("✅ Финальное видео с английскими словами создано!")
    
    def concat_videos(self, video_files, output_path):
        """Объединяет несколько видео файлов в один"""
        concat_list_file = os.path.join(APP_TEMP_PATH, "english_concat_list.txt")
        with open(concat_list_file, 'w') as f:
            for video_file in video_files:
                f.write(f"file '{os.path.abspath(video_file)}'\n")
        
        # Объединяем видео
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_file,
            '-c', 'copy', output_path, '-y'
        ], check=True)

class EnglishHorizontalVideoGenerator:
    def __init__(self):
        from config_english_horizontal import TEXT_POSITION
        self.width = TEXT_POSITION['screen']['width']
        self.height = TEXT_POSITION['screen']['height']
        self.duration_per_word = 3
        self.fps = 24
        
    def create_word_video_with_audio(self, word_data, audio_file, output_path):
        """Создает горизонтальное видео для одного английского слова с его аудио"""
        from text_renderer_english_horizontal import create_english_horizontal_text_block
        
        print(f"Создаем горизонтальное видео для слова: {word_data['english']}")
        
        # Создаем VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_path, fourcc, self.fps, (self.width, self.height))
        
        # Создаем изображение для слова
        pil_image = create_english_horizontal_text_block(word_data)
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        # Добавляем кадры
        frames_count = self.duration_per_word * self.fps
        for _ in range(int(frames_count)):
            video_writer.write(opencv_image)
        
        video_writer.release()
        
        # Добавляем аудио к видео
        final_video_path = output_path.replace('.mp4', '_with_audio.mp4')
        subprocess.run([
            'ffmpeg', '-i', output_path, '-i', audio_file,
            '-c:v', 'copy', '-c:a', 'aac', '-shortest',
            final_video_path, '-y'
        ], check=True)
        
        return final_video_path
    
    def generate_video_with_audio(self, words_data, output_path):
        """Генерирует финальное горизонтальное видео с аудио"""
        from audio_generator_english import generate_english_audio_for_words
        
        print("Генерируем аудио файлы...")
        audio_files = generate_english_audio_for_words(words_data)
        
        # Создаем видео для каждого слова с его аудио
        word_videos = []
        for i, (word, audio_info) in enumerate(zip(words_data, audio_files)):
            word_video_path = os.path.join(APP_TEMP_PATH, f"english_horizontal_word_{i+1}.mp4")
            final_word_video = self.create_word_video_with_audio(
                word, audio_info['file'], word_video_path
            )
            word_videos.append(final_word_video)
        
        # Объединяем все видео в одно
        self.concat_videos(word_videos, output_path)
        
        print("✅ Финальное горизонтальное видео с английскими словами создано!")
    
    def concat_videos(self, video_files, output_path):
        """Объединяет несколько видео файлов в один"""
        concat_list_file = os.path.join(APP_TEMP_PATH, "english_horizontal_concat_list.txt")
        with open(concat_list_file, 'w') as f:
            for video_file in video_files:
                f.write(f"file '{os.path.abspath(video_file)}'\n")
        
        subprocess.run([
            'ffmpeg', '-f', 'concat', '-safe', '0', '-i', concat_list_file,
            '-c', 'copy', output_path, '-y'
        ], check=True)

def create_english_video_from_data(words_data, output_path):
    """Основная функция для создания видео с английскими словами"""
    generator = EnglishVideoGenerator()
    generator.generate_video_with_audio(words_data, output_path)

def create_english_horizontal_video_from_data(words_data, output_path):
    """Основная функция для создания горизонтального видео с английскими словами"""
    generator = EnglishHorizontalVideoGenerator()
    generator.generate_video_with_audio(words_data, output_path)