import setuptools

setuptools.setup(
    name="btc-sim",
    version="0.0.1",
    author="Nathaniel Cherian",
    author_email="nathaniel@sylica.com",
    description="bitcoin simulator",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        'Development Status :: 3 - Alpha',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',

)