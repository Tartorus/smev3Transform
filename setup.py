import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="smev3Transform",
    version="1.0",
    author="Basharov Iliyas Ildarovich",
    author_email="5q00@mail.com",
    description="Пакет канонизации и нормализации xml элемента для подписания в СМЭВ 3.",
    install_requires=['lxml'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tartorus/smev3Transform",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
