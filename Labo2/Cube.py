# First we import the VTK Python package that will make available all
# of the VTK commands to Python.
import vtk
import random
import math

shapeModel = [
    [[3, 2, 2],
     [2, 2, 5],
     [5, 5, 5]],

    [[3, 0, 4],
     [3, 0, 4],
     [3, 1, 4]],
     
    [[6, 0, 4],
     [6, 6, 6],
     [1, 1, 1]]
]

def CreateVTKFragment():
    fragment = vtk.vtkCubeSource()
    fragment.SetXLength(1.0)
    fragment.SetYLength(1.0)
    fragment.SetZLength(1.0)
    return fragment

def CreateVTKShape(fragments):
    cubes = []

    appendFilter = vtk.vtkAppendPolyData()

    # Creating cubes and appending the Polydata
    for x, y, z in fragments:
        fragment = CreateVTKFragment()
        fragment.SetCenter(x, y, z)
        fragment.Update()
        cubes.append(fragment)
        # Appending the cubes
        appendFilter.AddInputData(fragment.GetOutput())

    appendFilter.Update()

    return appendFilter


def CreateShapeActor(fragments):
    poly = CreateVTKShape(fragments)

    # We send it to the mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(poly.GetOutputPort())

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    return actor


def GetShapeActors(cube):
    # Getting fragments position 
    shapes = {}
    for x, l1 in enumerate(cube):
        for y, l2 in enumerate(l1):
            for z, val in enumerate(l2):
                if(val not in shapes):
                    shapes[val] = []
                shapes[val].append([x, y, z])

    # Creating each shape
    actors = []
    for key, fragments in shapes.items():
        # Creating the actor
        a = CreateShapeActor(fragments)
        a.GetProperty().SetColor(random.random(), random.random(), random.random())
        actors.append(a)

    return actors


# Creating the actors shapes
actors = GetShapeActors(shapeModel)

# Creating a renderer for each step
renderers = []

for i in range(len(actors)):
    ren = vtk.vtkRenderer()
    ren.SetBackground(1, 1, 1) # White background
    renderers.append(ren)

    # Adding i actors
    for j in range(i + 1):
        # print(i)
        ren.AddActor(actors[j])



# Finally we create the render window which will show up on the screen
# We put our renderer into the render window using AddRenderer. We
# also set the size to be 800 pixels by 600.
renWin = vtk.vtkRenderWindow()

# ---- Creating a viewport for every renderer

# Number of column to display
col = 2
row = math.floor(len(actors)/col)
colSize = 1 / col
rowSize = 1 / (row + 1) 

# Steps
for i in range(row):
    for j in range(col):
        renderIndex = i * col + j
        ren = renderers[renderIndex]
        #ren.SetActiveCamera(camera)
        #ren.SetViewport(1 - rowSize - i * rowSize, j * colSize, 1 - i * rowSize, (j + 1) * colSize)
        ren.SetViewport(j * colSize, 1 - rowSize - i * rowSize, (j + 1) * colSize, 1 - i * rowSize,)        

# Solution 
renderers[len(renderers) - 1].SetViewport(0, 0, 1,rowSize)

# Adding the renderer to the window and setting the same camera for everybody

camera = vtk.vtkCamera()
camera.SetPosition(0, 0, 10)
camera.SetFocalPoint(1.5, 1.5, 1.5)
for ren in renderers:
    ren.SetActiveCamera(camera)
    renWin.AddRenderer(ren)


renWin.SetSize(800, 600)


'''
# Create the Renderer and assign actors to it. 
ren = vtk.vtkRenderer()
for actor in actors:
    ren.AddActor(actor)

ren.SetBackground(1, 1, 1)
'''

# used for interaction
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

iren.Initialize()
renWin.Render()
iren.Start()