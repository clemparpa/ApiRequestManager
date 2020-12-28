import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ApiRequestManager",
    version="1.0.4",
    author="clemparpa",
    author_email="clem.parpaillon@example.com",
    description="Communicate with Apis is easy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/clemparpa/PyApiManager",
    packages=[
        "ApiRequestManager",
        "src",
        "src/ApiConfig",
        "src/ApiRequest"
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