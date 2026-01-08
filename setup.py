from setuptools import setup, find_packages

setup(
    name="metaphlanplot",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "metaphlanplot=metaphlanplot.cli:main"
        ]
    },
)