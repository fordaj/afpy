import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="afpy",
    version="0.0.8",
    author="Andrew Ford",
    author_email="author@example.com",
    description="A personal python package for increasing python efficiency by simplifying repeatable code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fordaj/afpy",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)