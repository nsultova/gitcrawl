import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gitcrawl",
    version="0.1.2",
    author="Neda Sultova",
    author_email="n.sultova@hzdr.de",
    description="A small package for creating os-agnostic conda environment.yml files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nsultova/gitcrawl",
    packages=setuptools.find_packages(),
    package_data={"gitcrawl": ["python_module_index.pickle", "module-names.txt"]},
    install_requires=[
		"beautifulsoup4",
		"tqdm",
		"requests",
		"PyYAML",
		"requirements-parser",
		"pip-search",
		"findimports"
    ],
    entry_points={
        'console_scripts':[
            'gitcrawl=gitcrawl:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
