import os
from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


with open(os.path.dirname(__file__) + "/VERSION") as f:
    pkgversion = f.read().strip()


if 'ENGCOMMON_BRANCH' in os.environ:
    engcommon_branch = os.getenv("ENGCOMMON_BRANCH")
else:
    engcommon_branch = "main"


setup(
    name = "runxhpl",
    version = pkgversion,
    description = "High Performance Linpack Stress Test",
    url = "https://github.com/JustAddRobots/runxhpl",
    author = "Roderick Constance",
    author_email = "justaddrobots@icloud.com",
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    python_requires=">=3",
    packages = [
        "runxhpl",
    ],
    package_data = {
        "runxhpl": [
            "bin/xhpl-x86_64",
        ],
    },
    include_package_data = True,
    install_requires = [
        "docker",
        "engcommon @ git+https://github.com/JustAddRobots/engcommon.git@{0}".format(
            engcommon_branch
        ),
        "numpy",
    ],
    entry_points = {
        "console_scripts": [
            "runxhpl = runxhpl.cli:main",
        ]
    },
    zip_safe = False
)
