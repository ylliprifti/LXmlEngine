import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="dr-web-engine",
        version="0.1.3.Beta",
        author="Ylli Prifti",
        author_email="ylli@prifti.us",
        description="Data Retrieval Web Engine - Queryable Web Scrap engine build on python based on lxml and "
                    "Selenium package and using JSON as query construct.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ylliprifti/dr-web-engine",
        packages=setuptools.find_packages(),
        install_requires=['argparse', 'xvfbwrapper', 'selenium', 'python_interface',
                          'lxml', 'geckodriver_autoinstaller'],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
)
