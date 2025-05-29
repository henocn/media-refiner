 
from .core.engine import MediaRefinerEngine
from .utils.config import Config
from .utils.file_handler import FileHandler
from .processors.image_processor import ImageProcessor
from .processors.audio_processor import AudioProcessor
from .processors.video_processor import VideoProcessor


__version__ = "1.0.0"
__author__ = "Media Refiner Team"
__description__ = "Advanced media quality enhancement tool"


#------------------------------------------------------------------#
#                         Package Exports                          #
#------------------------------------------------------------------#
__all__ = [
    'MediaRefinerEngine',
    'Config',
    'FileHandler',
    'ImageProcessor',
    'AudioProcessor',
    'VideoProcessor',
    'refine_media',
    'refine_image',
    'refine_audio',
    'refine_video'
]


#------------------------------------------------------------------#
#                      Convenience Functions                       #
#------------------------------------------------------------------#
def refine_media(file_path, output_path=None, **options):
    engine = MediaRefinerEngine()
    engine.initialize()
    
    if options:
        engine.process_with_options([file_path], options)
    else:
        result = engine.process_single_file(file_path, output_path)
    
    engine.cleanup()
    return result


def refine_image(file_path, output_path=None, quality='high'):
    config = Config()
    config.image_quality = quality
    processor = ImageProcessor(config)
    
    if not output_path:
        file_handler = FileHandler(config)
        output_path = file_handler.generate_output_path(file_path)
    
    return processor.process_image(file_path, output_path)


def refine_audio(file_path, output_path=None, quality='high'):
    config = Config()
    config.audio_quality = quality
    processor = AudioProcessor(config)
    
    if not output_path:
        file_handler = FileHandler(config)
        output_path = file_handler.generate_output_path(file_path)
    
    return processor.process_audio(file_path, output_path)


def refine_video(file_path, output_path=None, quality='hd'):
    config = Config()
    config.video_quality = quality
    processor = VideoProcessor(config)
    
    if not output_path:
        file_handler = FileHandler(config)
        output_path = file_handler.generate_output_path(file_path)
    
    return processor.process_video(file_path, output_path)