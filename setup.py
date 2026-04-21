from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = [
        line.strip()
        for line in f.read().splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

setup(
    name="ANIME-RECOMMENDER",
    version="0.1",
    author="Le Trong Duc Anh",
    packages=find_packages(),
    install_requires = requirements,
)