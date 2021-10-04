from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = [
    "matplotlib",
    "numpy",
    "pandas",
    "selenium",
    "statsmodels",
    "sphinx",
    "sphinx-rtd-theme",
    "sphinxcontrib-bibtex",
    "typing-extensions"
]

setup(
    name="political_news_term_structure",
    version="0.6.18",
    author="Bernardo Paulsen for MBOCHIP",
    author_email="bernardo.paulsen@mbochip.com",
    description=(
        "Package that contains all custom package needed for the dissertation project,"
        " including web-scraping modules, vasicek module, etc."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ecompfin-ufrgs/political_news_term_structure/tree/second_version",
    packages=find_packages(),
    install_requires=requirements
    # classifiers=[
    #     "Programming Language :: Python :: 3.6"
    # ],
)