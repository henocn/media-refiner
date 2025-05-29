import os
import shutil
from pathlib import Path
from typing import List, Optional
import mimetypes




#------------------------------------------------------------------#
#                         File Handler                             #
#------------------------------------------------------------------#
class FileHandler:
    def __init__(self, config):
        self.config = config
        self.processed_files = []


    # Détection du type de média
    def detect_media_type(self, file_path: str) -> Optional[str]:
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type:
            if mime_type.startswith('video/'):
                return 'video'
            elif mime_type.startswith('audio/'):
                return 'audio'
            elif mime_type.startswith('image/'):
                return 'image'
        ext = Path(file_path).suffix.lower()
        if ext in self.config.supported_video_formats:
            return 'video'
        elif ext in self.config.supported_audio_formats:
            return 'audio'
        elif ext in self.config.supported_image_formats:
            return 'image'
        return None


    # Validation de l'existence du fichier
    def validate_file(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            return False
        if not os.path.isfile(file_path):
            return False
        return os.path.getsize(file_path) > 0


    # Génération du nom de fichier de sortie
    def generate_output_path(self, input_path: str, suffix: str = '_refined') -> str:
        path = Path(input_path)
        output_name = f"{path.stem}{suffix}{path.suffix}"
        return os.path.join(self.config.output_dir, output_name)


    # Sauvegarde du fichier original
    def backup_original(self, file_path: str) -> str:
        if not self.config.preserve_original:
            return file_path
        backup_dir = os.path.join(self.config.output_dir, 'originals')
        os.makedirs(backup_dir, exist_ok=True)
        backup_path = os.path.join(backup_dir, Path(file_path).name)
        shutil.copy2(file_path, backup_path)
        return backup_path


    # Nettoyage des fichiers temporaires
    def cleanup_temp_files(self):
        if os.path.exists(self.config.temp_dir):
            shutil.rmtree(self.config.temp_dir)
        os.makedirs(self.config.temp_dir, exist_ok=True)


    # Scan des fichiers dans un dossier
    def scan_directory(self, directory: str) -> List[str]:
        supported_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                if self.detect_media_type(file_path) and self.validate_file(file_path):
                    supported_files.append(file_path)
        return supported_files


    # Vérification de l'espace disque
    def check_disk_space(self, file_path: str, multiplier: float = 2.0) -> bool:
        file_size = os.path.getsize(file_path)
        required_space = file_size * multiplier
        free_space = shutil.disk_usage(self.config.output_dir).free
        return free_space > required_space


    # Enregistrement des fichiers traités
    def log_processed_file(self, input_path: str, output_path: str, status: str):
        self.processed_files.append({
            'input': input_path,
            'output': output_path,
            'status': status,
            'size_before': os.path.getsize(input_path) if os.path.exists(input_path) else 0,
            'size_after': os.path.getsize(output_path) if os.path.exists(output_path) else 0
        })
