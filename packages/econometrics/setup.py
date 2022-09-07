from setuptools import setup, find_packages

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()

setup(
    name="econometrics",
    version="0.0.0",
    author="Bernardo Paulsen",
    author_email="bernardopaulsen@gmail.com",
    description="",
    packages=find_packages(),
    install_requires=requirements
)
