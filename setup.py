import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upf_to_json",
    version="0.9.5",
    author="Simon Pintarelli",
    author_email="simon.pintarelli@cscs.ch",
    description="upf to json converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=[("", ["LICENSE"])],
    url="https://github.com/simonpintarelli/upf_to_json",
    packages=setuptools.find_packages(),
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'upf2json = upf_to_json.upf_to_json:cli'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering"
    ]

)
