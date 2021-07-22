from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

with open("requirements_dev.txt","r") as requirements_file:
    requirements = [line.rstrip() for line in requirements_file]

setup(
    name="news-brazil",
    version="0.1.0",
    author="Bernardo Paulsen",
    author_email="bernardopaulsen@gmail.com",
    description="A package to scrape brazilian news websites.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
    ],
)