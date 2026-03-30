from setuptools import find_packages, setup


def get_version():
    with open("pyplatzi/__init__.py") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"')
            
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Librería de Python para interactuar con la API de Platzi y gestionar cursos aprobados."

setup(
    name="pyplatzi",
    version=get_version(),
    author="CalumRakk",
    author_email="leocasti2@gmail.com",
    description="Herramienta CLI y librería para obtener cursos de Platzi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CalumRakk/pyplatzi",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.33.0",
        "pydantic>=2.12.5",
        "typer>=0.24.1"
    ],
    entry_points={
        "console_scripts": [
            "pyplatzi=pyplatzi.cli:run_script",
        ],
    }
)