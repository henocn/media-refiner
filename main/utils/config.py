import os
from pathlib import Path




#------------------------------------------------------------------#
#                        Configuration Manager                     #
#------------------------------------------------------------------#
class Config:
    def __init__(self):
        self.supported_video_formats = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']
        self.supported_audio_formats = ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a']
        self.supported_image_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
        self.output_dir = 'refined_media'
        self.temp_dir = 'temp_processing'
        self.video_quality = 'hd'
        self.audio_quality = 'high'
        self.image_quality = 'high'
        self.preserve_original = True


    # Validation du format de fichier
    def is_supported_format(self, file_path, media_type):
        ext = Path(file_path).suffix.lower()
        if media_type == 'video':
            return ext in self.supported_video_formats
        elif media_type == 'audio':
            return ext in self.supported_audio_formats
        elif media_type == 'image':
            return ext in self.supported_image_formats
        return False


    # Création des dossiers de sortie
    def ensure_output_dirs(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)


    # Configuration des paramètres de qualité vidéo
    def get_video_params(self):
        params = {
            'hd': {'width': 1280, 'height': 720, 'bitrate': '2500k'},
            'fhd': {'width': 1920, 'height': 1080, 'bitrate': '5000k'},
            '4k': {'width': 3840, 'height': 2160, 'bitrate': '15000k'}
        }
        return params.get(self.video_quality, params['hd'])


    # Configuration des paramètres de qualité audio
    def get_audio_params(self):
        params = {
            'medium': {'bitrate': '128k', 'sample_rate': 44100},
            'high': {'bitrate': '320k', 'sample_rate': 48000},
            'lossless': {'bitrate': '1411k', 'sample_rate': 96000}
        }
        return params.get(self.audio_quality, params['high'])


    # Configuration des paramètres de qualité image
    def get_image_params(self):
        params = {
            'medium': {'quality': 85, 'dpi': 150},
            'high': {'quality': 95, 'dpi': 300},
            'max': {'quality': 100, 'dpi': 600}
        }
        return params.get(self.image_quality, params['high'])
