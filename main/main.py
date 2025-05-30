import sys
import os
from .core.engine import MediaRefinerEngine
from .utils.config import Config




#------------------------------------------------------------------#
#                         Main Entry Point                         #
#------------------------------------------------------------------#
class MediaRefinerApp:
    def __init__(self):
        self.engine = MediaRefinerEngine()
        self.config = self.engine.config


    # Point d'entrée principal
    def run(self, args=None):
        if args is None:
            args = sys.argv[1:]
        
        if not args:
            self.show_help()
            return 1
        
        try:
            self.engine.initialize()
            result = self.parse_and_execute(args)
            self.engine.cleanup()
            return 0 if result else 1
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return 1


    # Analyse et exécution des arguments
    def parse_and_execute(self, args):
        command = args[0].lower()
        
        if command in ['help', '-h', '--help']:
            self.show_help()
            return True
        elif command in ['version', '-v', '--version']:
            self.show_version()
            return True
        elif command == 'file':
            return self.process_file(args[1:])
        elif command == 'dir':
            return self.process_directory(args[1:])
        elif command == 'batch':
            return self.process_batch_files(args[1:])
        else:
            return self.process_single_input(args)


    # Traitement d'un fichier unique
    def process_file(self, args):
        if not args:
            print("Error: No file specified")
            return False
        
        file_path = args[0]
        output_path = args[1] if len(args) > 1 else None
        options = self.parse_options(args[2:])
        
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return False
        
        print(f"Processing file: {file_path}")
        
        if options:
            result = self.engine.process_with_options([file_path], options)
            success = len(result['success']) > 0
        else:
            result = self.engine.process_single_file(file_path, output_path)
            success = result['status'] == 'success'
        
        if success:
            print(f"✓ File processed successfully")
            if 'output_path' in result:
                print(f"Output: {result['output_path']}")
        else:
            print(f"✗ Failed to process file")
            if 'error' in result:
                print(f"Error: {result['error']}")
        
        return success


    # Traitement d'un dossier
    def process_directory(self, args):
        if not args:
            print("Error: No directory specified")
            return False
        
        dir_path = args[0]
        options = self.parse_options(args[1:])
        recursive = options.get('recursive', True)
        max_workers = options.get('max_workers', 4)
        
        if not os.path.exists(dir_path):
            print(f"Error: Directory not found: {dir_path}")
            return False
        
        print(f"Processing directory: {dir_path}")
        result = self.engine.process_directory(dir_path, recursive, max_workers)
        
        if result.get('status') == 'failed':
            print(f"✗ {result['error']}")
            return False
        
        self.print_batch_results(result)
        return True


    # Traitement par lot
    def process_batch_files(self, args):
        if not args:
            print("Error: No files specified")
            return False
        
        file_paths = []
        options = {}
        
        for arg in args:
            if arg.startswith('--'):
                key, value = self.parse_option(arg)
                options[key] = value
            else:
                if os.path.exists(arg):
                    file_paths.append(arg)
                else:
                    print(f"Warning: File not found: {arg}")
        
        if not file_paths:
            print("Error: No valid files found")
            return False
        
        print(f"Processing {len(file_paths)} files...")
        
        if options:
            result = self.engine.process_with_options(file_paths, options)
        else:
            result = self.engine.process_batch(file_paths)
        
        self.print_batch_results(result)
        return len(result['success']) > 0


    # Traitement d'une entrée unique
    def process_single_input(self, args):
        input_path = args[0]
        
        if os.path.isfile(input_path):
            return self.process_file(args)
        elif os.path.isdir(input_path):
            return self.process_directory(args)
        else:
            print(f"Error: Path not found: {input_path}")
            return False


    # Analyse des options
    def parse_options(self, args):
        options = {}
        for arg in args:
            if arg.startswith('--'):
                key, value = self.parse_option(arg)
                options[key] = value
        return options


    # Analyse d'une option
    def parse_option(self, arg):
        if '=' in arg:
            key, value = arg[2:].split('=', 1)
        else:
            key = arg[2:]
            value = True
        
        if value in ['true', 'True', '1']:
            value = True
        elif value in ['false', 'False', '0']:
            value = False
        elif value.isdigit():
            value = int(value)
        
        return key, value


    # Affichage des résultats par lot
    def print_batch_results(self, result):
        total = len(result['success']) + len(result['failed'])
        success_count = len(result['success'])
        failed_count = len(result['failed'])
        
        print(f"\nResults:")
        print(f"✓ Processed: {success_count}/{total}")
        print(f"✗ Failed: {failed_count}/{total}")
        
        if failed_count > 0:
            print(f"\nFailed files:")
            for file_path in result['failed']:
                print(f"  - {file_path}")


    # Affichage de l'aide
    def show_help(self):
        help_text = """
Media Refiner - Advanced media quality enhancement tool

Usage:
  media-refiner <file_path> [output_path] [options]
  media-refiner file <file_path> [output_path] [options]
  media-refiner dir <directory_path> [options]
  media-refiner batch <file1> <file2> ... [options]

Options:
  --video-quality=<hd|fhd|4k>     Video quality preset
  --audio-quality=<medium|high|lossless>  Audio quality preset
  --image-quality=<medium|high|max>       Image quality preset
  --preserve-original=<true|false>        Keep original files
  --output-dir=<path>                     Output directory
  --max-workers=<number>                  Parallel processing threads
  --recursive=<true|false>                Process subdirectories

Examples:
  media-refiner video.mp4
  media-refiner file audio.mp3 enhanced_audio.mp3
  media-refiner dir ./media --video-quality=4k
  media-refiner batch *.jpg --image-quality=max
        """
        print(help_text)


    # Affichage de la version
    def show_version(self):
        from . import __version__
        print(f"Media Refiner v{__version__}")




#------------------------------------------------------------------#
#                         Entry Point Function                     #
#------------------------------------------------------------------#
def main():
    app = MediaRefinerApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
