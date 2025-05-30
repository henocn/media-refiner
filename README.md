# Media Refiner

Outil avancé d'amélioration de la qualité des médias pour vidéos, audio et images avec capacités d'upscaling HD+.

## Fonctionnalités

- **Amélioration Vidéo**: Upscaling HD/FHD/4K, réduction de bruit, stabilisation, amélioration du contraste
- **Amélioration Audio**: Réduction de bruit, amélioration de la clarté, égalisation, amélioration de la dynamique
- **Amélioration Image**: Netteté, débruitage, amélioration contraste/luminosité/saturation, upscaling
- **Traitement par Lot**: Traiter plusieurs fichiers ou dossiers entiers
- **Interface CLI**: Interface en ligne de commande facile à utiliser
- **Package Python**: Utiliser comme bibliothèque dans vos propres projets

## Installation

### Prérequis
- Python 3.8+
- FFmpeg (requis pour le traitement vidéo)

### Installer FFmpeg
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

### Installer Media Refiner
```bash
git clone https://github.com/henocn/media-refiner.git
cd media-refiner
pip install -e .
```

## Démarrage Rapide

### Utilisation en Ligne de Commande

**Traiter un seul fichier:**
```bash
media-refiner file video.mp4
media-refiner file audio.mp3 --audio-quality=lossless
media-refiner file image.jpg --image-quality=max
```

**Traiter un dossier:**
```bash
media-refiner directory ./media
media-refiner directory ./videos --video-quality=4k --recursive
```

**Traitement par lot:**
```bash
media-refiner batch *.mp4 *.avi --video-quality=fhd
media-refiner batch *.jpg *.png --image-quality=high
```

**Filtrer par type de média:**
```bash
media-refiner filter ./media --media-type=video --quality=4k
media-refiner filter ./media --media-type=audio --quality=lossless
```

**Obtenir des informations sur les médias:**
```bash
media-refiner info ./media
```

### Utilisation comme Bibliothèque Python

```python
from main import refine_media, MediaRefinerEngine

# Utilisation simple
result = refine_media('video.mp4', quality='4k')

# Utilisation avancée
engine = MediaRefinerEngine()
engine.initialize()

# Traiter un seul fichier
result = engine.process_single_file('video.mp4')

# Traiter un dossier
results = engine.process_directory('./media', recursive=True)

# Options personnalisées
options = {
    'video_quality': '4k',
    'audio_quality': 'lossless',
    'preserve_original': True,
    'max_workers': 8
}
results = engine.process_with_options(['file1.mp4', 'file2.mp4'], options)

engine.cleanup()
```

## Référence des Commandes

### Options Globales
- `--video-quality=<hd|fhd|4k>` - Préréglage qualité vidéo (défaut: hd)
- `--audio-quality=<medium|high|lossless>` - Préréglage qualité audio (défaut: high)
- `--image-quality=<medium|high|max>` - Préréglage qualité image (défaut: high)
- `--preserve-original=<true|false>` - Conserver les fichiers originaux (défaut: true)
- `--output-dir=<chemin>` - Dossier de sortie personnalisé
- `--max-workers=<nombre>` - Threads de traitement parallèle (défaut: 4)

### Commandes

#### `file` - Traiter un seul fichier
```bash
media-refiner file <fichier_entrée> [options]
media-refiner file video.mp4 --output=video_ameliore.mp4
```

#### `directory` - Traiter un dossier
```bash
media-refiner directory <chemin_dossier> [options]
media-refiner directory ./media --recursive --video-quality=4k
```

#### `batch` - Traiter plusieurs fichiers
```bash
media-refiner batch <fichier1> <fichier2> ... [options]
media-refiner batch *.mp4 --video-quality=fhd --max-workers=8
```

#### `filter` - Traiter par type de média
```bash
media-refiner filter <chemin> --media-type=<image|audio|video> [options]
media-refiner filter ./media --media-type=video --quality=4k
```

#### `info` - Afficher les informations des médias
```bash
media-refiner info <chemin>
```

## Préréglages de Qualité

### Qualité Vidéo
- **hd**: 1280x720, débit 2.5Mbps
- **fhd**: 1920x1080, débit 5Mbps  
- **4k**: 3840x2160, débit 15Mbps

### Qualité Audio
- **medium**: 128kbps, 44.1kHz
- **high**: 320kbps, 48kHz
- **lossless**: 1411kbps, 96kHz

### Qualité Image
- **medium**: qualité 85%, 150 DPI
- **high**: qualité 95%, 300 DPI
- **max**: qualité 100%, 600 DPI

## Formats Supportés

### Vidéo
- MP4, AVI, MKV, MOV, WMV, FLV, WebM

### Audio
- MP3, WAV, FLAC, AAC, OGG, M4A

### Image
- JPG, JPEG, PNG, BMP, TIFF, WebP

## Exemples

### Amélioration de Base
```bash
# Améliorer une vidéo en qualité HD
media-refiner file film.mp4 --video-quality=hd

# Améliorer un audio en haute qualité
media-refiner file chanson.mp3 --audio-quality=high

# Améliorer une image en qualité maximale
media-refiner file photo.jpg --image-quality=max
```

### Traitement par Lot
```bash
# Traiter toutes les vidéos d'un dossier en 4K
media-refiner directory ./videos --video-quality=4k

# Traiter toutes les images avec qualité maximale
media-refiner batch *.jpg *.png --image-quality=max

# Traiter seulement les fichiers audio d'un dossier
media-refiner filter ./media --media-type=audio --quality=lossless
```

### Options Avancées
```bash
# Dossier de sortie personnalisé avec 8 workers parallèles
media-refiner directory ./media --output-dir=./ameliore --max-workers=8

# Traiter sans conserver les originaux
media-refiner batch *.mp4 --preserve-original=false --video-quality=4k
```

## Structure de Sortie

```
refined_media/
├── fichiers_ameliores/
│   ├── video_refined.mp4
│   ├── audio_refined.wav
│   └── image_refined.jpg
└── originals/          # si preserve-original=true
    ├── video.mp4
    ├── audio.mp3
    └── image.jpg
```

## Conseils de Performance

1. **Utiliser plusieurs workers** pour le traitement par lot: `--max-workers=8`
2. **Traiter par type de média** pour une meilleure efficacité: `filter --media-type=video`
3. **Choisir des préréglages de qualité appropriés** selon vos besoins
4. **S'assurer d'avoir suffisamment d'espace disque** (2x la taille du fichier original recommandé)
5. **Utiliser un stockage SSD** pour un traitement plus rapide

## Dépannage

### Problèmes Courants

**FFmpeg introuvable:**
```bash
# Installer FFmpeg d'abord
winget install FFmpeg  # Windows
brew install ffmpeg    # macOS
sudo apt install ffmpeg # Linux
```

**Espace disque insuffisant:**
- Libérer de l'espace ou utiliser `--output-dir` pour spécifier un autre emplacement
- L'outil nécessite ~2x la taille du fichier original pour le traitement

**Problèmes de mémoire avec de gros fichiers:**
- Réduire la valeur `--max-workers`
- Traiter les fichiers individuellement au lieu du lot

**Format non supporté:**
- Vérifier la liste des formats supportés ci-dessus
- Convertir le fichier dans un format supporté d'abord

### Obtenir de l'Aide

```bash
media-refiner --help
media-refiner file --help
media-refiner directory --help
```

## Utilisation Avancée

### Configuration Personnalisée
```python
from main import Config, MediaRefinerEngine

# Configuration personnalisée
config = Config()
config.video_quality = '4k'
config.audio_quality = 'lossless'
config.preserve_original = False
config.output_dir = './mes_medias_ameliores'

engine = MediaRefinerEngine(config)
```

### Traitement avec Callbacks
```python
def progress_callback(current, total):
    print(f"Progression: {current}/{total}")

def completion_callback(result):
    if result['status'] == 'success':
        print(f"Succès: {result['output_path']}")
    else:
        print(f"Échec: {result['error']}")

# Utilisation avec callbacks (fonctionnalité future)
```

### Intégration dans vos Scripts
```python
import os
from main import MediaRefinerEngine

def ameliorer_dossier_media(chemin_dossier):
    engine = MediaRefinerEngine()
    engine.initialize()
    
    try:
        # Configurer la qualité selon le type
        engine.set_quality_settings(
            video_quality='4k',
            audio_quality='lossless',
            image_quality='max'
        )
        
        # Traiter le dossier
        results = engine.process_directory(chemin_dossier, recursive=True)
        
        # Générer un rapport
        rapport = engine.generate_report()
        print(f"Fichiers traités: {rapport['processed']}")
        print(f"Taux de succès: {rapport['success_rate']}%")
        
        return results
        
    finally:
        engine.cleanup()

# Utilisation
resultats = ameliorer_dossier_media('./mes_medias')
```

## API de la Bibliothèque

### Classes Principales

#### `MediaRefinerEngine`
Moteur principal pour le traitement des médias.

```python
engine = MediaRefinerEngine(config=None)
engine.initialize()
engine.process_single_file(file_path, output_path=None)
engine.process_batch(file_paths, max_workers=4)
engine.process_directory(directory_path, recursive=True, max_workers=4)
engine.cleanup()
```

#### `Config`
Configuration des paramètres de traitement.

```python
config = Config()
config.video_quality = 'hd'  # 'hd', 'fhd', '4k'
config.audio_quality = 'high'  # 'medium', 'high', 'lossless'
config.image_quality = 'high'  # 'medium', 'high', 'max'
config.preserve_original = True
config.output_dir = 'refined_media'
```

#### Processeurs Spécialisés

```python
from main.processors import ImageProcessor, AudioProcessor, VideoProcessor

# Traitement d'image uniquement
image_processor = ImageProcessor(config)
image_processor.process_image('photo.jpg', 'photo_amelioree.jpg')

# Traitement audio uniquement
audio_processor = AudioProcessor(config)
audio_processor.process_audio('chanson.mp3', 'chanson_amelioree.wav')

# Traitement vidéo uniquement
video_processor = VideoProcessor(config)
video_processor.process_video('film.mp4', 'film_ameliore.mp4')
```

## Licence

Licence MIT - voir le fichier LICENSE pour les détails.

## Contribution

1. Fork le dépôt
2. Créer une branche de fonctionnalité
3. Apporter des modifications en suivant le style de code
4. Soumettre une pull request

## Journal des Modifications

### v1.0.0
- Version initiale
- Amélioration vidéo, audio et image
- Interface CLI avec Click
- Support du traitement par lot
- Préréglages de qualité
- Interface de bibliothèque Python

## Support

Pour obtenir de l'aide ou signaler des bugs:
- GitHub Issues: https://github.com/henocn/media-refiner/issues
- Documentation: https://media-refiner.readthedocs.io/
- Email: support@media-refiner.com

## Remerciements

Merci aux bibliothèques open source qui rendent ce projet possible:
- OpenCV pour le traitement d'image et vidéo
- FFmpeg pour l'encodage vidéo
- librosa pour l'analyse audio
- Click pour l'interface CLI
- Et toutes les autres dépendances listées dans requirements.txt
