import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_requirements():
    with open('requirements.txt') as requirements:
        req = requirements.read().splitlines()
    return req

setuptools.setup(
    name="palantir-cli",
    version="0.0.2",
    author="Nathaniel Cherian",
    author_email="nathaniel@sylica.com",
    description="security analyzer and predictor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nathanielCherian/palantir",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',
    install_requires= get_requirements(),
    entry_points = {
        'console_scripts': ['palantir=cli.palantir:main'],
    },
    include_package_data=True,
)