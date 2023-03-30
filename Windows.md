```

set PIP_EXTRA_INDEX_URL=https://download.qt.io/official_releases/QtForPython/
set LD_LIBRARY_PATH=C:\Qt6\6.4.3\msvc2019_64\lib
set CMAKE_PREFIX_PATH=C:\Qt6\6.4.3\msvc2019_64\lib\cmake

pip install cmake_build_extension pyside6 shiboken6 shiboken6_generator
```

or PS 

```
$env:PIP_EXTRA_INDEX_URL='https://download.qt.io/official_releases/QtForPython/'
$env:LD_LIBRARY_PATH='C:\Qt6\6.4.3\msvc2019_64\lib'
$env:CMAKE_PREFIX_PATH='C:\Qt6\6.4.3\msvc2019_64\lib\cmake'
$env:CLANG_INSTALL_DIR='C:\Program Files\libclang-release_100-based-windows-vs2019_64\libclang\bin'
$env:PATH +=';C:\Program Files\libclang-release_100-based-windows-vs2019_64\libclang\bin'
pip install cmake_build_extension pyside6 shiboken6 shiboken6_generator
```

generate pyi:
```
shiboken6-genpyi.exe .\build\lib.win-amd64-cpython-310\PySide6QtAds\PySide6QtAds.pyd
```
ImportError: DLL load failed while importing PySide6QtAds