# pyside6_qtads
PySide6 wrapper for Qt Advanced Docking System

This module is currently little more than a proof-of-concept.

Uses [cmake-build-extension](https://github.com/diegoferigo/cmake-build-extension) to evoke [Shiboken](https://doc.qt.io/qtforpython/shiboken6/) to build a Python wrapper for [Qt-Advanced-Docking-System](https://github.com/githubuser0xFFFF/Qt-Advanced-Docking-System) for [Qt6](https://www.qt.io/).

PySide6 and Shiboken6 can be installed from pypi.org, but shiboken_generator cannot:

```sh
pip install --index-url=http://download.qt.io/official_releases/QtForPython/ --trusted-host download.qt.io shiboken6 pyside6 shiboken6_generator
```

This module is then build like so:

```sh
python setup.py {bdist_wheel|install} build_ext -D"CMAKE_PREFIX_PATH:PATH=/path/to/Qt/6.x.x/..."
```

or

```sh
pip {wheel|install} --global-option="build_ext" --global-option="-DCMAKE_PREFIX_PATH:PATH=/path/to/Qt/6.x.x/..." .
```

Any CMake flags needed to compile the Qt extension will need to be provided. This is likely at least CMAKE_PREFIX_PATH, as shown above.

---

Official Qt wheels do not target latest Python and may have old library deps. You can alternatively build from source.

1. Install Qt using the official installer

2. Download pyside source

```bash
	wget https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.4.0-src/pyside-setup-opensource-src-6.4.0.zip
	unzip pyside-setup-opensource-src-6.4.0.zip
```

3. Build & install pyside

```bash
	python setup.py install --qtpaths=$HOME/Qt/6.4.0/gcc_64/bin/qtpaths --ignore-git --build-tests --parallel=12 --verbose-build
```

Note: this will install pyside with all modules + shiboken6 and shiboken6-generator

4. Build and install `pyside6_qtads`

```bash
	python setup.py install build_ext -D"CMAKE_PREFIX_PATH:PATH=$HOME/Qt/6.4.0/gcc_64/lib/cmake"
```
