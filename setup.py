import os
from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


with open(os.path.dirname(__file__) + "/VERSION") as f:
    pkgversion = f.read().strip()


setup(
    name = "runxhpl",
    version = pkgversion,
    description = "High Performance Linpack Stress Test",
    url = ("git+ssh://git@{0}.github.com/"
           "JustAddRobots/{0}.git@{1}").format(name, pkgversion),
    author = "Roderick Constance",
    author_email = "justaddrobots@icloud.com"
    license = "Private",
    packages = [
        "{0}".format(name),
    ],
    package_data = {
        "runxhpl": [
            "bin/xhpl-x86_64-avx512",
        ],
    },
    include_package_data = True,
    install_requires = [
        "docker",
        "engcommon @ git+ssh://git@engcommon.github.com/JustAddRobots/engcommon.git",
        "numpy",
    ],
    entry_points = {
        "console_scripts": [
            "runxhpl = runxhpl.cli:main",
        ]
    },
    zip_safe = False,
)
