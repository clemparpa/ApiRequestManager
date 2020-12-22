import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyApiManager-clemparpa",
    version="0.5.1",
    author="clemparpa",
    author_email="clem.parpaillon@example.com",
    description="Communicate with Apis is Ez",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clemparpa/PyApiManager",
    packages=[
        "PyApiManager",
        "PyApiManager_src",
        "PyApiManager_src/ApiConfig",
        "PyApiManager_src/ApiRequest"
    ],
    install_requires=[
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)