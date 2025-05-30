from setuptools import setup, find_packages
import os


def read_requirements():
    with open('requirements.txt', 'r') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def read_readme():
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "Advanced media quality enhancement tool"


#------------------------------------------------------------------#
#                         Package Setup                            #
#------------------------------------------------------------------#
setup(
    name="media-refiner",
    version="1.0.0",
    author="Media Refiner Team",
    author_email="ngasamah@gmail.com",
    description="Advanced media quality enhancement tool for videos, audio and images",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/media-refiner/media-refiner",
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
    install_requires=read_requirements(),
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
        "Source": "https://github.com/henocn/media-refiner.git",
    },
)
