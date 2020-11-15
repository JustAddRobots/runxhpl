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
    url = ("git+ssh://git@runxhpl.github.com/"
           "JustAddRobots/runxhpl.git@{0}").format(pkgversion),
    author = "Roderick Constance",
    author_email = "justaddrobots@icloud.com",
    license = "Private",
    packages = [
        "runxhpl",
    ],
    package_data = {
        "runxhpl": [
            "bin/mpirun",
            "bin/mpiexec.hydra",
            "bin/xhpl-x86_64-avx",
            "bin/xhpl-x86_64-core-avx512",
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
