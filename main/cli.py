import click
import os
import sys
from .core.engine import MediaRefinerEngine
from .utils.config import Config
from . import __version__




#------------------------------------------------------------------#
#                         CLI Interface                            #
#------------------------------------------------------------------#
@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help='Show version')
@click.pass_context
def cli(ctx, version):
    if version:
        click.echo(f"Media Refiner v{__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file path')
@click.option('--video-quality', type=click.Choice(['hd', 'fhd', '4k']), default='hd', help='Video quality preset')
@click.option('--audio-quality', type=click.Choice(['medium', 'high', 'lossless']), default='high', help='Audio quality preset')
@click.option('--image-quality', type=click.Choice(['medium', 'high', 'max']), default='high', help='Image quality preset')
@click.option('--preserve-original/--no-preserve-original', default=True, help='Keep original files')
@click.option('--output-dir', type=click.Path(), help='Output directory')
def file(file_path, output, video_quality, audio_quality, image_quality, preserve_original, output_dir):
    """Process a single media file"""
    engine = MediaRefinerEngine()
    
    if output_dir:
        engine.config.output_dir = output_dir
    
    engine.config.video_quality = video_quality
    engine.config.audio_quality = audio_quality
    engine.config.image_quality = image_quality
    engine.config.preserve_original = preserve_original
    
    try:
        engine.initialize()
        
        with click.progressbar(length=1, label='Processing file') as bar:
            result = engine.process_single_file(file_path, output)
            bar.update(1)
        
        if result['status'] == 'success':
            click.echo(f"✓ File processed successfully: {result['output_path']}")
        else:
            click.echo(f"✗ Failed to process file: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
    
    finally:
        engine.cleanup()


@cli.command()
@click.argument('directory_path', type=click.Path(exists=True, file_okay=False))
@click.option('--recursive/--no-recursive', default=True, help='Process subdirectories')
@click.option('--video-quality', type=click.Choice(['hd', 'fhd', '4k']), default='hd', help='Video quality preset')
@click.option('--audio-quality', type=click.Choice(['medium', 'high', 'lossless']), default='high', help='Audio quality preset')
@click.option('--image-quality', type=click.Choice(['medium', 'high', 'max']), default='high', help='Image quality preset')
@click.option('--preserve-original/--no-preserve-original', default=True, help='Keep original files')
@click.option('--output-dir', type=click.Path(), help='Output directory')
@click.option('--max-workers', type=int, default=4, help='Number of parallel workers')
def directory(directory_path, recursive, video_quality, audio_quality, image_quality, preserve_original, output_dir, max_workers):
    """Process all media files in a directory"""
    engine = MediaRefinerEngine()
    
    if output_dir:
        engine.config.output_dir = output_dir
    
    engine.config.video_quality = video_quality
    engine.config.audio_quality = audio_quality
    engine.config.image_quality = image_quality
    engine.config.preserve_original = preserve_original
    
    try:
        engine.initialize()
        
        click.echo(f"Scanning directory: {directory_path}")
        result = engine.process_directory(directory_path, recursive, max_workers)
        
        if result.get('status') == 'failed':
            click.echo(f"✗ {result['error']}")
            sys.exit(1)
        
        print_results(result)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
    
    finally:
        engine.cleanup()


@cli.command()
@click.argument('files', nargs=-1, required=True, type=click.Path(exists=True))
@click.option('--video-quality', type=click.Choice(['hd', 'fhd', '4k']), default='hd', help='Video quality preset')
@click.option('--audio-quality', type=click.Choice(['medium', 'high', 'lossless']), default='high', help='Audio quality preset')
@click.option('--image-quality', type=click.Choice(['medium', 'high', 'max']), default='high', help='Image quality preset')
@click.option('--preserve-original/--no-preserve-original', default=True, help='Keep original files')
@click.option('--output-dir', type=click.Path(), help='Output directory')
@click.option('--max-workers', type=int, default=4, help='Number of parallel workers')
def batch(files, video_quality, audio_quality, image_quality, preserve_original, output_dir, max_workers):
    """Process multiple media files"""
    engine = MediaRefinerEngine()
    
    if output_dir:
        engine.config.output_dir = output_dir
    
    engine.config.video_quality = video_quality
    engine.config.audio_quality = audio_quality
    engine.config.image_quality = image_quality
    engine.config.preserve_original = preserve_original
    
    try:
        engine.initialize()
        
        valid_files = [f for f in files if os.path.isfile(f)]
        if not valid_files:
            click.echo("No valid files found")
            sys.exit(1)
        
        click.echo(f"Processing {len(valid_files)} files...")
        result = engine.process_batch(valid_files, max_workers)
        
        print_results(result)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
    
    finally:
        engine.cleanup()


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--media-type', type=click.Choice(['image', 'audio', 'video']), required=True, help='Media type to process')
@click.option('--quality', type=str, help='Quality preset for the media type')
@click.option('--output-dir', type=click.Path(), help='Output directory')
def filter(input_path, media_type, quality, output_dir):
    """Process files by media type"""
    engine = MediaRefinerEngine()
    
    if output_dir:
        engine.config.output_dir = output_dir
    
    if quality:
        if media_type == 'video':
            engine.config.video_quality = quality
        elif media_type == 'audio':
            engine.config.audio_quality = quality
        elif media_type == 'image':
            engine.config.image_quality = quality
    
    try:
        engine.initialize()
        
        if os.path.isfile(input_path):
            file_paths = [input_path]
        else:
            file_paths = engine.file_handler.scan_directory(input_path)
        
        result = engine.process_by_media_type(file_paths, media_type)
        
        if result.get('status') == 'failed':
            click.echo(f"✗ {result['error']}")
            sys.exit(1)
        
        print_results(result)
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)
    
    finally:
        engine.cleanup()


@cli.command()
@click.argument('input_path', type=click.Path(exists=True))
def info(input_path):
    """Show information about media files"""
    engine = MediaRefinerEngine()
    
    try:
        if os.path.isfile(input_path):
            file_paths = [input_path]
        else:
            file_paths = engine.file_handler.scan_directory(input_path)
        
        click.echo(f"Media files found: {len(file_paths)}")
        
        types_count = {'image': 0, 'audio': 0, 'video': 0}
        total_size = 0
        
        for file_path in file_paths:
            media_type = engine.file_handler.detect_media_type(file_path)
            if media_type:
                types_count[media_type] += 1
                total_size += os.path.getsize(file_path)
        
        click.echo(f"Images: {types_count['image']}")
        click.echo(f"Audio files: {types_count['audio']}")
        click.echo(f"Video files: {types_count['video']}")
        click.echo(f"Total size: {format_size(total_size)}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}")
        sys.exit(1)



#------------------------------------------------------------------#
#                         Helper Functions                         #
#------------------------------------------------------------------#
def print_results(result):
    total = len(result['success']) + len(result['failed'])
    success_count = len(result['success'])
    failed_count = len(result['failed'])
    
    click.echo(f"\nResults:")
    click.echo(f"✓ Processed: {success_count}/{total}")
    click.echo(f"✗ Failed: {failed_count}/{total}")
    
    if failed_count > 0:
        click.echo(f"\nFailed files:")
        for file_path in result['failed']:
            click.echo(f"  - {file_path}")


def format_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"


if __name__ == '__main__':
    cli()
