from setuptools import setup

# Load packages from requirements.txt
with open("requirements.txt", "r") as file:
    required_packages = [ln.strip() for ln in file.readlines()]

setup(
    python_requires='>=3.8.8',
    install_requires=[required_packages]
)
