#!/usr/bin/env python3
import inspect
import os
import subprocess
import sys
from distutils.cmd import Command as _Command
from pathlib import Path
from typing import List, Any

import cmake_build_extension
import setuptools
from wheel.bdist_wheel import bdist_wheel

import PySide6
import shiboken6

if os.getenv('PYSIDE6_QTADS_NO_HARD_PYSIDE_REQUIREMENT'):
    install_requirements = [
        'PySide6-Essentials', 'shiboken6'
    ]
else:
    install_requirements = [
        f'PySide6-Essentials=={PySide6.__version__}',
        f'shiboken6=={shiboken6.__version__}'
    ]


class bdist_wheel_abi3(bdist_wheel):
    def get_tag(self):
        python, abi, plat = super().get_tag()

        if python.startswith("cp"):
            # on CPython, our wheels are abi3 and compatible back to 3.6
            return "cp37", "abi3", plat

        return python, abi, plat


class CustomCMakeExtension(cmake_build_extension.CMakeExtension):
    """XXX: Override CMakeExtension to support extra kwargs"""

    def __init__(
            self,
            name: str,
            install_prefix: str = "",
            disable_editable: bool = False,
            write_top_level_init: str = None,
            cmake_configure_options: List[str] = (),
            source_dir: str = str(Path(".").absolute()),
            cmake_build_type: str = "Release",
            cmake_component: str = None,
            cmake_depends_on: List[str] = (),
            expose_binaries: List[str] = (),
            cmake_generator: str = "Ninja",
            **kwargs
    ):
        setuptools.Extension.__init__(self, name=name, sources=[], **kwargs)

        if not Path(source_dir).is_absolute():
            source_dir = str(Path(".").absolute() / source_dir)

        if not Path(source_dir).absolute().is_dir():
            raise ValueError(f"Directory '{source_dir}' does not exist")

        self.install_prefix = install_prefix
        self.cmake_build_type = cmake_build_type
        self.disable_editable = disable_editable
        self.write_top_level_init = write_top_level_init
        self.cmake_depends_on = cmake_depends_on
        self.source_dir = str(Path(source_dir).absolute())
        self.cmake_configure_options = cmake_configure_options
        self.cmake_component = cmake_component
        self.expose_binaries = expose_binaries
        self.cmake_generator = cmake_generator


init_py = Path("init.py").read_text()


class CustomBuildCommand(setuptools.Command):
    """A custom command that ensures that build_ext is executed before build_py."""

    description = 'Build package'
    user_options = []

    def finalize_options(self) -> None:
        pass

    def initialize_options(self) -> None:
        pass

    def run(self):
        self.run_command('install')
        p = subprocess.run(r"python .\support\generate_pyi.py --sys-path .\build\temp.win-amd64-cpython-310 PySide6QtAds", shell=True)
        self.run_command('bdist_wheel')


setuptools.setup(
    ext_modules=[
        CustomCMakeExtension(
            name="PySide6-QtAds",
            install_prefix="PySide6QtAds",
            write_top_level_init=init_py,
            source_dir=str(Path(__file__).parent.absolute()),
            cmake_configure_options=[
                "-DBUILD_EXAMPLES:BOOL=OFF",
                "-DBUILD_STATIC:BOOL=ON",
                "-DADS_VERSION=4.0.1",
                f"-DPython3_ROOT_DIR={Path(sys.prefix)}"
            ],
            py_limited_api=True
        ),
    ],
    cmdclass=dict(
        build_all=CustomBuildCommand,
        build_ext=cmake_build_extension.BuildExtension,
        bdist_wheel=bdist_wheel_abi3
    ),
    install_requires=install_requirements,
)
