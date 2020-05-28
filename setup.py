import setuptools

from setuptools import setup, find_packages
setup(
    name='dr-web-engine',
    packages=find_packages(),
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="dr-web-engine",  # Replace with your own username
        version="V0.1.beta",
        author="Ylli Prifti",
        author_email="ylli@prifti.us",
        description="Data Retreival Web Engine - Queryable Web Scrap engine build on python based on lxml package and using JSON as query construct.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ylliprifti/dr-web-engine",
        download_url='https://github.com/ylliprifti/dr-web-engine/archive/V0.1.beta.tar.gz',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
)
