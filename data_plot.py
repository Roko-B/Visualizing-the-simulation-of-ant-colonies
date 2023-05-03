from backend import DiffPair, InteractivePlot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mplW

#defining the differential equations
def foodDiff(colony, foodParam): return -foodParam*colony
def colonyDiff(food, colonyParam): return colonyParam*food
diffEquations = [foodDiff, colonyDiff]
startingState = [2,2]
parameters = [1,2]
dt = 0.01
#------------------------------------------------------------------------------------------------------
diffPair = DiffPair(10, dt, diffEquations, startingState, parameters)
xData, yData = diffPair.getData()
diffPair.logData('results.txt', "FOOD", "COLONY")

fig, ax = plt.subplots(); plt.grid()
line, = ax.plot(xData, yData, lw = 1.5); point, = ax.plot(xData[0], yData[0], "ro", markersize = 8);
ax.set_aspect(1) #set this to "auto" for more extreme parameter values such as [0,100] and set it to 1 if you want to showcase the shape of the graph

ax.set_xlabel("Food")
ax.set_ylabel("Colony")
ax.set_title("Phase space of ant colonies")
plt.subplots_adjust(left=0.25, bottom=0.2)

#making the vector field by using the values of the system of differential equations as the directional components
xLim = ax.get_xlim(); yLim = ax.get_ylim()
xMesh, yMesh = np.meshgrid(
	np.arange(xLim[0]-1, xLim[1]+1, (xLim[1]-xLim[0]+2)/20),
	np.arange(yLim[0]-1,yLim[1]+1, (yLim[1]-yLim[0]+2)/20)
)

u = foodDiff(yMesh, parameters[0])
v = colonyDiff(xMesh, parameters[1])

quiver = ax.quiver(
	xMesh, yMesh, u, v,
	angles = 'xy', scale_units = "xy", width = 0.003, alpha = 0.5
)
quiverData = [quiver, xMesh, yMesh]

#setting up the sliders and buttons
timeStepSlider = mplW.Slider(
	ax = plt.axes([0.25,0.05,0.65,0.03]),
	label = "dt",
	valmin = 0,
	valmax = 0.1,
	valinit = dt
)
foodParamSlider = mplW.Slider(
	ax = plt.axes([0.25/4, 0.25, 0.02, 0.63]),
	label = "a",
	valmin = 0,
	valmax = max(parameters),
	valinit = parameters[0],
	orientation = "vertical"
)
colonyParamSlider = mplW.Slider(
	ax = plt.axes([0.25*2/4, 0.25, 0.02, 0.63]),
	label = "b",
	valmin = 0, #change to a negative number if you want to make the model of a single colony and food a model of two competing colonies
	valmax = max(parameters),
	valinit = parameters[1],
	orientation = "vertical"
)
resetButton = mplW.Button(plt.axes([0.25/4, 0.05, 0.25/4+0.02, 0.04]), "Reset", hovercolor = "0.7")

#drawing everything
paramSliders = [foodParamSlider, colonyParamSlider]
interactivePlot = InteractivePlot(line, point, quiverData, diffPair, paramSliders, timeStepSlider, resetButton)
interactivePlot.connect()
plt.show()
