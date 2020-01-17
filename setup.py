import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cimico", 
    version="1.0.1",
    author="knightron0",
    entry_points = {
        'console_scripts': ['cimico = cimico.main:main'],
    },
    author_email="sarthak.robo@gmail.com",
    description="A simple python debugger that generates a video of the program running along with valuable information.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CCExtractor/cimico",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pillow', 'opencv-python'],
)