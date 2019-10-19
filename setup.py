import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="upf_to_json",
    version="0.9.1",
    author="Simon Pintarelli",
    author_email="simon.pintarelli@cscs.ch",
    description="upf to json converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    data_files=[("", ["LICENSE"])],
    url="https://github.com/simonpintarelli/upf_to_json",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
