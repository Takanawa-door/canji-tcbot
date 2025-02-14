from setuptools import setup, find_packages

setup(
    name="tcbot",
    version="1.0.4",
    packages=find_packages(),
    install_requires = [
        "selenium>=4.28.1",
        "colorama>=0.4.6"
    ]
)