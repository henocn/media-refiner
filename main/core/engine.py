from ..utils.config import Config
from ..utils.file_handler import FileHandler
from ..processors.image_processor import ImageProcessor
from ..processors.audio_processor import AudioProcessor
from ..processors.video_processor import VideoProcessor
from tqdm import tqdm
import os
import threading
from concurrent.futures import ThreadPoolExecutor




#------------------------------------------------------------------#
#                         Media Refiner Engine                     #
#------------------------------------------------------------------#
class MediaRefinerEngine:
    def __init__(self, config=None):
        self.config = config or Config()
        self.file_handler = FileHandler(self.config)
        self.image_processor = ImageProcessor(self.config)
        self.audio_processor = AudioProcessor(self.config)
        self.video_processor = VideoProcessor(self.config)
        self.results = {'processed': 0, 'failed': 0, 'skipped': 0}


    # Initialisation de l'environnement
    def initialize(self):
        self.config.ensure_output_dirs()
        self.file_handler.cleanup_temp_files()


    # Traitement d'un fichier unique
    def process_single_file(self, file_path: str, output_path: str = None) -> dict:
        if not self.file_handler.validate_file(file_path):
            return {'status': 'failed', 'error': 'Invalid file'}
        
        media_type = self.file_handler.detect_media_type(file_path)
        if not media_type:
            return {'status': 'failed', 'error': 'Unsupported format'}
        
        if not self.file_handler.check_disk_space(file_path):
            return {'status': 'failed', 'error': 'Insufficient disk space'}
        
        if not output_path:
            output_path = self.file_handler.generate_output_path(file_path)
        
        backup_path = self.file_handler.backup_original(file_path)
        
        success = False
        if media_type == 'image':
            success = self.image_processor.process_image(file_path, output_path)
        elif media_type == 'audio':
            success = self.audio_processor.process_audio(file_path, output_path)
        elif media_type == 'video':
            success = self.video_processor.process_video(file_path, output_path)
        
        status = 'success' if success else 'failed'
        self.file_handler.log_processed_file(file_path, output_path, status)
        
        return {
            'status': status,
            'input_path': file_path,
            'output_path': output_path if success else None,
            'backup_path': backup_path,
            'media_type': media_type
        }


    # Traitement par lot avec barre de progression
    def process_batch(self, file_paths: list, max_workers: int = 4) -> dict:
        results = {'success': [], 'failed': [], 'details': []}
        
        with tqdm(total=len(file_paths), desc="Processing files") as pbar:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.process_single_file, path): path for path in file_paths}
                
                for future in futures:
                    result = future.result()
                    results['details'].append(result)
                    
                    if result['status'] == 'success':
                        results['success'].append(result['output_path'])
                        self.results['processed'] += 1
                    else:
                        results['failed'].append(result['input_path'])
                        self.results['failed'] += 1
                    
                    pbar.update(1)
        
        return results


    # Traitement d'un dossier
    def process_directory(self, directory_path: str, recursive: bool = True, max_workers: int = 4) -> dict:
        if not os.path.exists(directory_path):
            return {'status': 'failed', 'error': 'Directory not found'}
        
        file_paths = self.file_handler.scan_directory(directory_path) if recursive else []
        if not recursive:
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                if os.path.isfile(file_path) and self.file_handler.detect_media_type(file_path):
                    file_paths.append(file_path)
        
        if not file_paths:
            return {'status': 'failed', 'error': 'No supported files found'}
        
        return self.process_batch(file_paths, max_workers)


    # Traitement par type de média
    def process_by_media_type(self, file_paths: list, media_type: str) -> dict:
        filtered_paths = []
        for path in file_paths:
            detected_type = self.file_handler.detect_media_type(path)
            if detected_type == media_type:
                filtered_paths.append(path)
        
        if not filtered_paths:
            return {'status': 'failed', 'error': f'No {media_type} files found'}
        
        return self.process_batch(filtered_paths)


    # Configuration des paramètres de qualité
    def set_quality_settings(self, video_quality: str = None, audio_quality: str = None, image_quality: str = None):
        if video_quality:
            self.config.video_quality = video_quality
        if audio_quality:
            self.config.audio_quality = audio_quality
        if image_quality:
            self.config.image_quality = image_quality


    # Génération du rapport de traitement
    def generate_report(self) -> dict:
        total_files = sum(self.results.values())
        success_rate = (self.results['processed'] / total_files * 100) if total_files > 0 else 0
        
        report = {
            'total_files': total_files,
            'processed': self.results['processed'],
            'failed': self.results['failed'],
            'skipped': self.results['skipped'],
            'success_rate': round(success_rate, 2),
            'processed_files': self.file_handler.processed_files
        }
        
        return report


    # Nettoyage final
    def cleanup(self):
        self.file_handler.cleanup_temp_files()


    # Traitement avec options avancées
    def process_with_options(self, file_paths: list, options: dict) -> dict:
        if 'video_quality' in options:
            self.config.video_quality = options['video_quality']
        if 'audio_quality' in options:
            self.config.audio_quality = options['audio_quality']
        if 'image_quality' in options:
            self.config.image_quality = options['image_quality']
        if 'preserve_original' in options:
            self.config.preserve_original = options['preserve_original']
        if 'output_dir' in options:
            self.config.output_dir = options['output_dir']
            self.config.ensure_output_dirs()
        
        max_workers = options.get('max_workers', 4)
        return self.process_batch(file_paths, max_workers)
