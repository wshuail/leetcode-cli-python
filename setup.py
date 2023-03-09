import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="leetcode_cli",
    version="0.0.1",
    author="Luke Wang",
    author_email="lukewangdata@gmaile.com",
    description=("A command line tool for Leetcode based on Python"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wshuail/leetcode-cli-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords=['Leetcode', 'Command Line', 'Python'],
    install_requires=["requests", "bs4"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "lc = leetcode_cli.cli:main",
        ]
    },
    license='GPL'
)
