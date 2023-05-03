import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mplW

#defines the class known as differential equation pair or DiffPair for short. This class is built in such a way that you can make multiple changes to its state and you will only have to recalculate the data once making the process more efficient by avoiding needless computation.
class DiffPair:
	def __init__(self, t, dt, diffPair, startingState, parameters):
		self.t = t
		self.dt = dt
		self.diffPair = diffPair
		self.startingState = startingState
		self.parameters = parameters
		self.updateData()

	def getState(self): return {
		"t": self.t,
		"dt": self.dt,
		"diffPair": self.diffPair,
		"startingState": self.startingState,
		"parameters": self.parameters,
	}
	
	def getData(self): return self.data

	def setState(self, diffPairState):
		self.t = diffPairState["t"]
		self.dt = diffPairState["dt"]
		self.diffPair = diffPairState["diffPair"]
		self.startingState = diffPairState["startingState"]
		self.parameters = diffPairState["parameters"]
	
	def updateData(self):
		state = [self.startingState[0], self.startingState[1]] #the state is copied in this weird way to avoid copying by reference, which introduces numerous bugs
		xData = [self.startingState[0]]
		yData = [self.startingState[1]]

		#since we do not know the analytical solution to the equations we can approximate it by using the fact that dF=-aC*dt and dC=bF*dt to find the small changes to F and C. Because the derivatives get more accurate the smaller the time step is we use small time steps to approximate the solution and it's evolution.
		for timeStep in np.arange(0, self.t, self.dt):
			#calculate derivative at point x_t, y_t
			dx = self.diffPair[0](state[1], self.parameters[0])
			dy = self.diffPair[1](state[0], self.parameters[1])
			
			#calculate the change to the individual function values and add them to previous function values
			state[0]+=dx*self.dt
			state[1]+=dy*self.dt

			xData.append(state[0])
			yData.append(state[1])
		#final data estimates the data gotten by using the analytical solution of the pair od diff equations
		self.data = [xData, yData]

	def logData(self, fileName, label1, label2):
		#logs the data using the provided labels and file names, intended for careful analysis of the data. 
		file = open(fileName, "w")
		for i in range(0, len(self.data[0]) - 1):
			file.write(f"{label1}: {self.data[0][i]}, {label2}: {self.data[1][i]}\n")
		file.write(f"{label1}: {self.data[0][-1]}, {label2}: {self.data[1][-1]}")
		file.close()

#defines the interactive plot class which handles all of the interactivity for the plot.
class InteractivePlot:
	def __init__(self, line, point, quiverData, diffPair, paramSliders, timeStepSlider, resetButton):
		self.line = line
		self.point = point
		self.quiverData = quiverData
		self.diffPair = diffPair
		self.diffPairStateInitial = diffPair.getState()
		self.paramSliders = paramSliders
		self.timeStepSlider = timeStepSlider
		self.resetButton = resetButton
		self.pressData = None

	def connect(self):
		#enables the registering of the events by the interactive plot child
		self.cidPress = self.line.figure.canvas.mpl_connect("button_press_event", self.onPress)
		self.cidRelease = self.line.figure.canvas.mpl_connect("button_release_event", self.onRelease)
		self.cidMotion = self.line.figure.canvas.mpl_connect("motion_notify_event", self.onMotion)
		self.resetButton.on_clicked(self.onResetButtonClick)
		self.timeStepSlider.on_changed(self.onSliderUpdate)
		for slider in self.paramSliders:
			slider.on_changed(self.onSliderUpdate)

	def updatePlot(self):
		#uses saved state info to update data and plot it again
		self.diffPair.updateData()
		xData, yData = self.diffPair.getData()
		self.line.set_xdata(xData)
		self.line.set_ydata(yData)
		self.point.set_xdata([xData[0]])
		self.point.set_ydata([yData[0]])

		plt.draw()
	
	def updateQuiver(self):
		#updates the quiver directions using xMesh(quiverData[1]) and yMesh(quiverData[2] together with the two differential equations and the updated parameters)
		state = self.diffPair.getState()
		self.quiverData[0].set_UVC(
			state["diffPair"][0](self.quiverData[2], state["parameters"][0]),
			state["diffPair"][1](self.quiverData[1], state["parameters"][1]),
		)

		plt.draw()

	#slider and button handling functions
	def onResetButtonClick(self, event):
		#uses info of the initial state to reset the plot
		self.paramSliders[0].set_val(self.diffPairStateInitial["parameters"][0])
		self.paramSliders[1].set_val(self.diffPairStateInitial["parameters"][1])
		self.timeStepSlider.set_val(self.diffPairStateInitial["dt"])

		self.diffPair.setState(self.diffPairStateInitial)
		self.updatePlot()
		self.updateQuiver()

	def onSliderUpdate(self, value):
		#changes the values when sliders are moved
		sliderValues =  [slider.val for slider in self.paramSliders]
		if 0 in sliderValues or self.timeStepSlider.val == 0 : return
		
		state = self.diffPair.getState()
		state["parameters"] = sliderValues
		state["dt"] = self.timeStepSlider.val

		self.diffPair.setState(state)
		self.updatePlot()
		self.updateQuiver()

	#movement handling functions
	def onPress(self, event):
		#stores the coordinates of the press and the center of the dot in a 2 dimensional tuple
		if event.inaxes != self.point.axes: return
		contains, details = self.point.contains(event)
		if not contains: return

		self.pressData = (
			(self.point.get_xdata()[0], self.point.get_ydata()[0]), (event.xdata, event.ydata))
		# print(self.pressData)

	def onMotion(self, event):
		if self.pressData is None or event.inaxes!=self.point.axes: return

		#calculates the difference between the position after movement and the position of the click, once it has that it adds it to the center of the point thus moving it to our desired coordinates.
		(x0, y0), (xPress, yPress) = self.pressData
		dx = event.xdata - xPress
		dy = event.ydata - yPress
		state = self.diffPair.getState()
		state["startingState"] = [x0 + dx, y0 + dy]

		self.diffPair.setState(state)
		self.updatePlot()

	def onRelease(self, event):
		#sets the pressData variable to be None thus cancelling the movement
		self.pressData = None
		self.updatePlot()
