# Media Refiner

Advanced media quality enhancement tool for videos, audio and images with HD+ upscaling capabilities.

## Features

- **Video Enhancement**: HD/FHD/4K upscaling, noise reduction, stabilization, contrast enhancement
- **Audio Enhancement**: Noise reduction, clarity improvement, equalization, dynamic range enhancement
- **Image Enhancement**: Sharpening, denoising, contrast/brightness/saturation enhancement, upscaling
- **Batch Processing**: Process multiple files or entire directories
- **CLI Interface**: Easy-to-use command line interface
- **Python Package**: Use as a library in your own projects

## Installation

### Requirements
- Python 3.8+
- FFmpeg (required for video processing)

### Install FFmpeg
**Windows:**
```bash
winget install FFmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### Install Media Refiner
```bash
git clone https://github.com/henocn/media-refiner.git
cd media-refiner
pip install -e .
```

## Quick Start

### Command Line Usage

**Process a single file:**
```bash
media-refiner file video.mp4
media-refiner file audio.mp3 --audio-quality=lossless
media-refiner file image.jpg --image-quality=max
```

**Process a directory:**
```bash
media-refiner directory ./media
media-refiner directory ./videos --video-quality=4k --recursive
```

**Batch processing:**
```bash
media-refiner batch *.mp4 *.avi --video-quality=fhd
media-refiner batch *.jpg *.png --image-quality=high
```

**Filter by media type:**
```bash
media-refiner filter ./media --media-type=video --quality=4k
media-refiner filter ./media --media-type=audio --quality=lossless
```

**Get media information:**
```bash
media-refiner info ./media
```

### Python Library Usage

```python
from main import refine_media, MediaRefinerEngine

# Simple usage
result = refine_media('video.mp4', quality='4k')

# Advanced usage
engine = MediaRefinerEngine()
engine.initialize()

# Process single file
result = engine.process_single_file('video.mp4')

# Process directory
results = engine.process_directory('./media', recursive=True)

# Custom options
options = {
    'video_quality': '4k',
    'audio_quality': 'lossless',
    'preserve_original': True,
    'max_workers': 8
}
results = engine.process_with_options(['file1.mp4', 'file2.mp4'], options)

engine.cleanup()
```

## Command Reference

### Global Options
- `--video-quality=<hd|fhd|4k>` - Video quality preset (default: hd)
- `--audio-quality=<medium|high|lossless>` - Audio quality preset (default: high)
- `--image-quality=<medium|high|max>` - Image quality preset (default: high)
- `--preserve-original=<true|false>` - Keep original files (default: true)
- `--output-dir=<path>` - Custom output directory
- `--max-workers=<number>` - Parallel processing threads (default: 4)

### Commands

#### `file` - Process single file
```bash
media-refiner file <input_file> [options]
media-refiner file video.mp4 --output=enhanced_video.mp4
```

#### `directory` - Process directory
```bash
media-refiner directory <directory_path> [options]
media-refiner directory ./media --recursive --video-quality=4k
```

#### `batch` - Process multiple files
```bash
media-refiner batch <file1> <file2> ... [options]
media-refiner batch *.mp4 --video-quality=fhd --max-workers=8
```

#### `filter` - Process by media type
```bash
media-refiner filter <path> --media-type=<image|audio|video> [options]
media-refiner filter ./media --media-type=video --quality=4k
```

#### `info` - Show media information
```bash
media-refiner info <path>
```

## Quality Presets

### Video Quality
- **hd**: 1280x720, 2.5Mbps bitrate
- **fhd**: 1920x1080, 5Mbps bitrate  
- **4k**: 3840x2160, 15Mbps bitrate

### Audio Quality
- **medium**: 128kbps, 44.1kHz
- **high**: 320kbps, 48kHz
- **lossless**: 1411kbps, 96kHz

### Image Quality
- **medium**: 85% quality, 150 DPI
- **high**: 95% quality, 300 DPI
- **max**: 100% quality, 600 DPI

## Supported Formats

### Video
- MP4, AVI, MKV, MOV, WMV, FLV, WebM

### Audio
- MP3, WAV, FLAC, AAC, OGG, M4A

### Image
- JPG, JPEG, PNG, BMP, TIFF, WebP

## Examples

### Basic Enhancement
```bash
# Enhance video to HD quality
media-refiner file movie.mp4 --video-quality=hd

# Enhance audio to high quality
media-refiner file song.mp3 --audio-quality=high

# Enhance image to maximum quality
media-refiner file photo.jpg --image-quality=max
```

### Batch Processing
```bash
# Process all videos in directory to 4K
media-refiner directory ./videos --video-quality=4k

# Process all images with maximum quality
media-refiner batch *.jpg *.png --image-quality=max

# Process only audio files in directory
media-refiner filter ./media --media-type=audio --quality=lossless
```

### Advanced Options
```bash
# Custom output directory with 8 parallel workers
media-refiner directory ./media --output-dir=./enhanced --max-workers=8

# Process without preserving originals
media-refiner batch *.mp4 --preserve-original=false --video-quality=4k
```

## Output Structure

```
refined_media/
├── enhanced_files/
│   ├── video_refined.mp4
│   ├── audio_refined.wav
│   └── image_refined.jpg
└── originals/          # if preserve-original=true
    ├── video.mp4
    ├── audio.mp3
    └── image.jpg
```

## Performance Tips

1. **Use multiple workers** for batch processing: `--max-workers=8`
2. **Process by media type** for better efficiency: `filter --media-type=video`
3. **Choose appropriate quality** presets based on your needs
4. **Ensure sufficient disk space** (2x original file size recommended)
5. **Use SSD storage** for faster processing

## Troubleshooting

### Common Issues

**FFmpeg not found:**
```bash
# Install FFmpeg first
winget install FFmpeg  # Windows
brew install ffmpeg    # macOS
sudo apt install ffmpeg # Linux
```

**Insufficient disk space:**
- Free up space or use `--output-dir` to specify different location
- Tool requires ~2x original file size for processing

**Memory issues with large files:**
- Reduce `--max-workers` value
- Process files individually instead of batch

**Unsupported format:**
- Check supported formats list above
- Convert file to supported format first

### Getting Help

```bash
media-refiner --help
media-refiner file --help
media-refiner directory --help
```

## License

MIT License - see LICENSE file for details.

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes following the code style
4. Submit pull request

## Changelog

### v1.0.0
- Initial release
- Video, audio, and image enhancement
- CLI interface with Click
- Batch processing support
- Quality presets
- Python library interface
