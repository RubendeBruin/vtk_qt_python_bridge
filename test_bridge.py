import sys
from pathlib import Path
import os

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from shiboken6 import wrapInstance, getCppPointer

# Built module (from cpp_bridge/build/<config>)
os.add_dll_directory(r"C:/debug/vtkdock/VTK/build-bridge/bin/Release")
os.add_dll_directory(r"C:/Qt/6.10.2/msvc2022_64/bin")
os.add_dll_directory(r"C:/debug/vtkdock/.venv/Lib/site-packages/PySide6")
sys.path.insert(0, str(Path(__file__).resolve().parent / "build" / "Release"))
import vtk_qt_bridge


def main() -> int:
    app = QApplication(sys.argv)

    window = QMainWindow()
    host = QWidget(window)
    layout = QVBoxLayout(host)

    parent_ptr = int(getCppPointer(host)[0])
    widget_ptr = vtk_qt_bridge.create_widget(parent_ptr)

    vtk_widget = wrapInstance(int(widget_ptr), QWidget)
    layout.addWidget(vtk_widget)

    window.setCentralWidget(host)
    window.resize(900, 700)
    window.show()

    code = app.exec()
    vtk_qt_bridge.delete_widget(widget_ptr)
    return code


if __name__ == "__main__":
    raise SystemExit(main())
