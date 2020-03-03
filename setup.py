from setuptools import setup


with open("README.md") as fd:
    long_description = fd.read()

setup(
        name='fuzzy_systems',
        version='0.3.0',
        url="https://github.com/byteofsoren/python_fuzzy_system",
        author="Magnus Sörensen",
        author_email="byteofsoren@gmail.com",
        description='A fuzzy system for python with fuzzy reasoning and classification.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        py_modules=["fuzzy_system"],
        package_dir={'':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX",
            ]
        )
