from setuptools import find_packages, setup

try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Librería de Python para interactuar con la API de Platzi y gestionar cursos aprobados."

setup(
    name="pyplatzi",
    version="0.1.0",
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
        "requests>=2.31.0",
        "pydantic>=2.0.0",
        "typer[all]>=0.9.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "pyplatzi=pyplatzi.cli:run_script",
        ],
    },
    include_package_data=True,
)