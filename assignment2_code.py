# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 17:00:26 2019

@author: 17807
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 06:58:47 2019

@author: gauravi
"""

import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()

# Setting the background color as black for all ports
ColorBackground = [0.0, 0.0, 0.0]

# Create the reader for the data
PathDicom = "CT"
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(PathDicom)
reader.Update()



### Core Logic for Port 1: Volume Rendering
# Creating view port 1
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

# Mapping of the mapper to the actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)

# Setting the camera
camera =vtk.vtkCamera ();
camera.SetPosition(0, 0,100);
camera.SetFocalPoint(0, 0, 0);

# Create transfer mapping scalar value to opacity with the provided values
opacityTransferFunction = vtk.vtkPiecewiseFunction()
opacityTransferFunction.AddPoint(-3024,   0.0)
opacityTransferFunction.AddPoint(-77,   0.0)
opacityTransferFunction.AddPoint(180,   0.2)
opacityTransferFunction.AddPoint(260,   0.4)
opacityTransferFunction.AddPoint(3071,   0.8)

# Create transfer mapping scalar value to color with the provided values
colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(-77, 0.5, 0.2, 0.1)
colorTransferFunction.AddRGBPoint(180, 0.9, 0.6, 0.3)
colorTransferFunction.AddRGBPoint(179, 1.0, 0.9, 0.9)
colorTransferFunction.AddRGBPoint(260, 0.6, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(3071, 0.8, 0.7, 0.1)

# The property describes how the data will look
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetColor(colorTransferFunction)
volumeProperty.SetScalarOpacity(opacityTransferFunction)
volumeProperty.ShadeOn()
volumeProperty.SetInterpolationTypeToLinear()

# The mapper / ray cast function know how to render the data
volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
volumeMapper.SetBlendModeToComposite()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# The volume holds the mapper and the property and
# can be used to position/orient the volume
volume = vtk.vtkVolume()
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)



## Creating view port 2
actor1 = vtk.vtkMarchingCubes()
actor1.SetInputConnection(reader.GetOutputPort())
actor1.ComputeGradientsOn()
actor1.ComputeScalarsOff()
actor1.SetValue(0, 300)
    
# Polydata mapper for the iso-surface
mapperIso = vtk.vtkPolyDataMapper()
mapperIso.SetInputConnection(actor1.GetOutputPort())
mapperIso.ScalarVisibilityOff()

# Actor for the iso surface
actorIso = vtk.vtkActor()
actorIso.SetMapper(mapperIso)
actorIso.GetProperty().SetColor(1.,1.,1.)



# Create the standard renderer, render window and interactor
ren1 = vtk.vtkRenderer()
ren1.AddVolume(volume)
ren1.SetActiveCamera(camera);
ren1.GetActiveCamera().Zoom(0.9)
ren1.ResetCamera()
ren1.SetViewport(0, 0, 0.33, 1)
ren1.SetBackground(ColorBackground)


# Rendering second view port
ren2 = vtk.vtkRenderer()
ren2.SetActiveCamera(ren1.GetActiveCamera()) # set the viewport 2 to same view as camera 1
ren2.SetViewport(0.33, 0, 0.66, 1)
ren2.AddActor(actorIso)
ren2.SetBackground(ColorBackground)


# Rendering third view port
ren = vtk.vtkRenderer()
ren.SetActiveCamera(ren1.GetActiveCamera())  # set the viewport 3 to same view as camera 1
ren.SetBackground(ColorBackground)
ren.SetViewport(0.66, 0, 1, 1)
ren.AddVolume(volume)
ren.AddActor(actorIso)


# Defining a rendering window
renWin = vtk.vtkRenderWindow()
renWin.SetSize(1500, 1500)


# Adding rendering elements to the window
renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren)

renWin.Render()


# Setting up an user interface interactor and passing it a rendering window as input
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)



# Exporting the rendered scene to a JPG ﬁle
w2i = vtk.vtkWindowToImageFilter()
w2i.SetInput(renWin)
w2i.Update()
writer = vtk.vtkJPEGWriter()
writer.SetInputConnection(w2i.GetOutputPort())
# Note: This file will be saved in the same location where you place the .py file
writer.SetFileName("JPG_of_Rendered_Scene.jpg")
renWin.Render()
writer.Write()



# finally enable user interface interactor
iren.Initialize()
iren.Start()
