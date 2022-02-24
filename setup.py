# -*- coding: utf-8 -*-

import re
import setuptools
from parver import Version, ParseError

# Build a wheel file containing the source code using the following command in a terminal:
# >>> python setup.py bdist_wheel

namespace = 'seeq.*'

with open("README.md", "r") as fh:
    long_description = fh.read()

version_scope = {'__builtins__': None}
with open('seeq/addons/udf_ui/_version.py', "r+") as f:
    version_file = f.read()
    version_line = re.search(r"__version__ = (.*)", version_file)
    if version_line is None:
        raise ValueError(f"Invalid version. Expected __version__ = 'xx.xx.xx', but got \n{version_file}")
    version = version_line.group(1).replace(" ", "").strip('\n').strip("'").strip('"')
    print(f"version: {version}")
    Version.parse(version)
    exec(version_line.group(0), version_scope)

setup_args = dict(
    name='seeq-udf-ui',
    version=version_scope['__version__'],
    description='A Seeq add-on tool for managing user-defined formula functions.',
    author='Ehsan Shahidi',
    author_email="ehsan.shahidi@seeq.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seeq12/udf-ui",
    packages=setuptools.find_namespace_packages(include=[namespace]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "ipywidgets>=7.6.3",
        "ipyvuetify>=1.8.0",
        "rx>=3.2.0",
        "traitlets>=5.1.0",
        "IPython>=7.25.0",
        "typeguard>=2.13.0",
        "mixpanel>=4.9.0",
        "Markdown>=3.3.4",
        "unmarkd==0.1.7"
    ],  
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    license='Apache License 2.0'
)

setuptools.setup(**setup_args)
