"""
Setup script for Adaptive Ensemble Sudoku Solver.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="adaptive-ensemble-sudoku-solver",
    version="1.0.0",
    author="Research Team",
    author_email="research@example.com",
    description="An Adaptive and Intelligent Ensemble Framework for Efficient Sudoku Solving",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IH-Arik/Adaptive-Ensemble-Sudoku-Solver",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Games/Entertainment :: Puzzle Games",
        "Topic :: Education",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.910",
        ],
        "visualization": [
            "matplotlib>=3.5.0",
            "seaborn>=0.11.0",
            "pandas>=1.3.0",
        ],
        "profiling": [
            "psutil>=5.8.0",
            "memory-profiler>=0.60.0",
        ],
        "gui-alternatives": [
            "PyQt5>=5.15.0",
            "kivy>=2.1.0",
        ],
        "packaging": [
            "pyinstaller>=4.5.0",
            "cx-freeze>=6.10",
        ],
    },
    entry_points={
        "console_scripts": [
            "sudoku-solver=src.cli.main:main",
            "sudoku-benchmark=src.cli.benchmark:main",
            "sudoku-generate=src.cli.generate:main",
        ],
    },
    include_package_data=True,
    package_data={
        "src": ["data/*.txt", "data/*.json"],
    },
)
