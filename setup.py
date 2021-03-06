# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from glob import glob
import os
from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from setuptools.command.develop import develop
import sys

from maro import __version__

# root path to backend
BASE_SRC_PATH = "./maro/backends"
# backend module name
BASE_MODULE_NAME = "maro.backends"

# extensions to be compiled
extensions = []
cython_directives = {"embedsignature": True}
compile_conditions = {}

# CURRENTLY we using environment variables to specified compiling conditions
# TODO: used command line arguments instead

# specified frame backend
FRAME_BACKEND = os.environ.get("FRAME_BACKEND", "NUMPY")  # NUMPY or empty


# include dirs for frame and its backend
include_dirs = []

# backend base extensions
extensions.append(
    Extension(
        f"{BASE_MODULE_NAME}.backend",
        sources = [f"{BASE_SRC_PATH}/backend.c"])
)

if FRAME_BACKEND == "NUMPY":
    import numpy

    include_dirs.append(numpy.get_include())

    extensions.append(
        Extension(
            f"{BASE_MODULE_NAME}.np_backend",
            sources = [f"{BASE_SRC_PATH}/np_backend.c"],
            define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
            include_dirs = include_dirs)
    )
else:
    # raw implementation
    # NOTE: not implemented now
    extensions.append(
        Extension(
            f"{BASE_MODULE_NAME}.raw_backend",
            sources = [f"{BASE_SRC_PATH}/raw_backend.c"])
    )

# frame
extensions.append(
    Extension(
        f"{BASE_MODULE_NAME}.frame",
        sources = [f"{BASE_SRC_PATH}/frame.c"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        include_dirs=include_dirs)
)

setup(
    name="maro",
    version=__version__,
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    author="",
    author_email="",
    url="",
    project_urls={
        "Code": "/path/to/code/repo",
        "Issues": "/path/to/issues",
        "Documents": "/path/to/documents"
    },
    license="",
    platforms=[],
    keywords=[],
    classifiers=[
        # See <https://pypi.org/classifiers/> for all classifiers
        "Programing Language :: Python",
        "Programing Language :: Python :: 3"
    ],
    python_requires=">=3.6,<3.8",
    setup_requires=[
        "numpy==1.19.1",
        "PyYAML==5.3.1"
    ],
    install_requires=[
        # TODO: use a helper function to collect these
        "numpy==1.19.1",
        "torch==1.6.0",
        "holidays==0.10.3",
        "pyaml==20.4.0",
        "redis==3.5.3",
        "pyzmq==19.0.2",
        "requests==2.24.0",
        "psutil==5.7.2",
        "deepdiff==5.0.2",
        "azure-storage-blob==12.3.2",
        "azure-storage-common==2.1.0",
        "geopy==2.0.0",
        "pandas==0.25.3",
        "PyYAML==5.3.1"
    ],
    entry_points={
        "console_scripts": [
            "maro=maro.cli.maro:main",
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "maro.simulator.scenarios.ecr": ["topologies/*/*.yml", "meta/*.yml"],
        "maro.simulator.scenarios.citi_bike": ["topologies/*/*.yml", "meta/*.yml"],
        "maro.cli.k8s": ["lib/**/*"],
        "maro.cli.grass": ["lib/**/*"],
    },
    zip_safe=False,
    ext_modules=extensions,
)
