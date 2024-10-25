"""Script to install local packages
"""
import setuptools

def parse_requirements_file(filename):
    with open(filename) as fid:
        requires = [l.strip() for l in fid.readlines() if not l.startswith("#")]
    return requires

install_requires = parse_requirements_file("requirements.txt")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

authors = {
    "Karimi": ("Fariba Karimi", "karimi@csh.ac.at"),
    "Martin-Gutierrez": ("Samuel Martin-Gutierrez", "martin.gutierrez@csh.ac.at"),
    "Cartier van Dissel": ("Mauritz Cartier van Dissel", "cartiervandissel@csh.ac.at"),}

setuptools.setup(
    name="multisoc",
    version="0.1.1",
    author=authors["Martin-Gutierrez"][0],
    author_email=authors["Martin-Gutierrez"][1],
    description=("A package to simulate and analyze networks with multidimensional interactions."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CSHVienna/multisoc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    python_requires=">=3.9",
)