"""
Установочный скрипт для mozgach108
"""

from setuptools import setup, find_packages
import os

# Читаем README для длинного описания
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Читаем requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mozgach108",
    version="1.0.0",
    author="Mozgach108 Team",
    author_email="thai@nativemind.net",
    description="Система из 108 квантово-запутанных языковых моделей",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/braindler/mozgach108",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.4.0",
        ],
        "gpu": [
            "torch-audio>=2.0.0",
            "torch-vision>=0.15.0",
        ],
        "quantum": [
            "qiskit>=0.45.0",
            "qiskit-aer>=0.12.0",
            "cirq>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mozgach108=mozgach108.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "mozgach108": [
            "config/*.json",
            "models/*.json",
            "categories/*.md",
            "docs/*.md",
        ],
    },
    zip_safe=False,
)
