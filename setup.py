from setuptools import find_packages, setup

setup(
    name="bakatools",
    version="0.0.1",
    author="Piotr Bakalarski",
    author_email="piotrb5e3+pypi@gmail.com",
    description="My tools for solving programming puzzles",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
