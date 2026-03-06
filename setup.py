from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="workiz",
    version="0.1.0",
    author="Okoya Usman",
    author_email="",
    description="A Python wrapper for the Workiz RESTful API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/okoyausman/workiz-python-wrapper",
    project_urls={
        "Bug Tracker": "https://github.com/okoyausman/workiz-python-wrapper/issues",
        "Documentation": "https://github.com/okoyausman/workiz-python-wrapper#readme",
        "Source Code": "https://github.com/okoyausman/workiz-python-wrapper",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
)