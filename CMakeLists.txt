cmake_minimum_required(VERSION 3.24)
project(vtk_qt_bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)
find_package(VTK REQUIRED COMPONENTS
  CommonCore
  RenderingCore
  RenderingOpenGL2
  GUISupportQt
)
find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets OpenGL OpenGLWidgets)

pybind11_add_module(vtk_qt_bridge src/bridge_widget.cpp)

target_link_libraries(vtk_qt_bridge PRIVATE
  Qt6::Core
  Qt6::Gui
  Qt6::Widgets
  Qt6::OpenGL
  Qt6::OpenGLWidgets
  VTK::CommonCore
  VTK::RenderingCore
  VTK::RenderingOpenGL2
  VTK::GUISupportQt
)

target_include_directories(vtk_qt_bridge PRIVATE ${VTK_INCLUDE_DIRS})

target_compile_definitions(vtk_qt_bridge PRIVATE
  NOMINMAX
  WIN32_LEAN_AND_MEAN
)
