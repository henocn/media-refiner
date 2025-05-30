from setuptools import setup, find_packages
import os


def read_readme():
    if os.path.exists('README.md'):
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                return f.read()
        except:
            pass
    return "Outil avancé d'amélioration de la qualité des médias pour vidéos, audio et images"


#------------------------------------------------------------------#
#                         Package Setup                            #
#------------------------------------------------------------------#
setup(
    name="media-refiner",
    version="1.0.0",
    author="Henoc N'GASAMA",
    author_email="ngasamah@gmail.com",
    description="Outil avancé d'amélioration de la qualité des médias pour vidéos, audio et images",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/henocn/media-refiner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "pillow>=10.0.0",
        "librosa>=0.10.0",
        "soundfile>=0.12.0",
        "scipy>=1.10.0",
        "pydub>=0.25.0",
        "moviepy==1.0.3",
        "ffmpeg-python>=0.2.0",
        "tqdm>=4.65.0",
        "click>=8.1.0",
        "scikit-image>=0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "media-refiner=main.cli:cli",
            "media-refiner-app=main.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "main": ["*.txt", "*.md"],
    },
    keywords=[
        "media",
        "video",
        "audio", 
        "image",
        "enhancement",
        "quality",
        "processing",
        "refiner",
        "upscale",
        "denoise",
        "cli"
    ],
    project_urls={
        "Bug Reports": "https://github.com/henocn/media-refiner/issues",
        "Source": "https://github.com/henocn/media-refiner",
        "Documentation": "https://media-refiner.readthedocs.io/",
    },
)
