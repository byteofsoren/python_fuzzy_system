from setuptools import setup


with open("README.md") as fd:
    long_description = fd.read()

setup(
        name='Python_fuzzy_systems',
        version='0.0.2',
        description='A fuzzy system for python with fuzzy reasoning and classification.',
        long_description=long_description,
        long_description_content_type="text/markdown",
        py_modules=["python_fuzzy_system"],
        package_dir={'':'src'},
        classifiers=[
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS independent",
            ]
        )
