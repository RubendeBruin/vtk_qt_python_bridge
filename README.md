# Native Qt/VTK Bridge (Option 2)

This folder contains a minimal C++ Python extension (`vtk_qt_bridge`) that creates a
`QVTKOpenGLNativeWidget` and returns its raw pointer to Python. Python can wrap the
pointer into a `QWidget` using `shiboken6.wrapInstance`.

## Why this exists

`VTK::GUISupportQt` is marked `EXCLUDE_WRAP` for Python in VTK, so the C++ adapter
classes are not directly available from `vtkmodules` Python bindings. This bridge
exposes a tiny C++ API instead.

## Current status in this environment

- Qt SDK installed: `C:\Qt\6.10.2\msvc2022_64`
- VTK configured against Qt successfully in `VTK/build-bridge`
- `vtk_qt_bridge` compiled successfully in `cpp_bridge/build/Release`

At runtime, the Python process needs DLL search paths for:

- `C:\debug\vtkdock\VTK\build-bridge\bin\Release`
- `C:\Qt\6.10.2\msvc2022_64\bin`
- `C:\debug\vtkdock\.venv\Lib\site-packages\PySide6`

`test_bridge.py` already adds these via `os.add_dll_directory(...)`.

## Prerequisites

1. Visual Studio C++ toolchain.
2. Qt 6 SDK with CMake package files (`Qt6Config.cmake`) and import libs.
3. A VTK C++ build that includes `GUISupportQt`.

## Suggested build flow

```powershell
# In a VS developer prompt (or call vcvars64.bat first)
cmake -S VTK -B VTK/build-bridge \
  -DVTK_BUILD_TESTING=OFF \
  -DVTK_BUILD_EXAMPLES=OFF \
  -DVTK_BUILD_ALL_MODULES=OFF \
  -DVTK_GROUP_ENABLE_Qt=WANT \
  -DVTK_MODULE_ENABLE_VTK_GUISupportQt=YES \
  -DCMAKE_PREFIX_PATH="<path-to-Qt6-cmake-prefix>" \
  -DCMAKE_INSTALL_PREFIX=C:/debug/vtkdock/vtk-install-bridge

cmake --build VTK/build-bridge --config Release --target vtkGUISupportQt -j 10

cmake -S cpp_bridge -B cpp_bridge/build \
  -Dpybind11_DIR=C:/debug/vtkdock/.venv/Lib/site-packages/pybind11/share/cmake/pybind11 \
  -DVTK_DIR=C:/debug/vtkdock/VTK/build-bridge/lib/cmake/vtk-9.6 \
  -DCMAKE_PREFIX_PATH=C:/Qt/6.10.2/msvc2022_64

cmake --build cpp_bridge/build --config Release
```

## Usage after build

```powershell
./cpp_bridge/runtime_env.ps1
C:/debug/vtkdock/.venv/Scripts/python.exe cpp_bridge/test_bridge.py
```
