#include <pybind11/pybind11.h>

#include <QWidget>

#include <QVTKOpenGLNativeWidget.h>
#include <vtkGenericOpenGLRenderWindow.h>
#include <vtkNew.h>
#include <vtkRenderer.h>

namespace py = pybind11;

namespace {
quintptr create_widget(quintptr parent_ptr)
{
  auto* parent = reinterpret_cast<QWidget*>(parent_ptr);
  auto* widget = new QVTKOpenGLNativeWidget(parent);

  vtkNew<vtkGenericOpenGLRenderWindow> rw;
  vtkNew<vtkRenderer> renderer;
  renderer->SetBackground(0.12, 0.18, 0.28);
  rw->AddRenderer(renderer);

  widget->setRenderWindow(rw);
  widget->show();
  return reinterpret_cast<quintptr>(widget);
}

void delete_widget(quintptr widget_ptr)
{
  auto* widget = reinterpret_cast<QWidget*>(widget_ptr);
  delete widget;
}
}

PYBIND11_MODULE(vtk_qt_bridge, m)
{
  m.doc() = "Minimal native Qt/VTK bridge";
  m.def("create_widget", &create_widget, py::arg("parent_ptr") = 0);
  m.def("delete_widget", &delete_widget, py::arg("widget_ptr"));
}
