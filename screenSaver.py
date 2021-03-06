from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3,LineSegs,NodePath


class MyApp(ShowBase):
	def __init__(self):
		ShowBase.__init__(self)

		# Load the environment model.
		self.scene = self.loader.loadModel("models/environment")
		# Reparent the model to render.
		self.scene.reparentTo(self.render)
		# Apply scale and position transforms on the model.
		self.scene.setScale(0.25, 0.25, 0.25)
		self.scene.setPos(-8, 42, 0)

		# Load and transform the panda actor.
		self.pandaActor = Actor("models/panda-model",
								{"walk": "models/panda-walk4"})
		self.pandaActor.setScale(0.005, 0.005, 0.005)
		self.pandaActor.reparentTo(self.render)
		# Loop its animation.
		self.pandaActor.loop("walk")

		# Create the four lerp intervals needed for the panda to
		# walk back and forth.
		posInterval1 = self.pandaActor.posInterval(13,
												   Point3(0, -10, 0),
												   startPos=Point3(0, 10, 0))
		posInterval2 = self.pandaActor.posInterval(13,
												   Point3(0, 10, 0),
												   startPos=Point3(0, -10, 0))
		hprInterval1 = self.pandaActor.hprInterval(3,
												   Point3(180, 0, 0),
												   startHpr=Point3(0, 0, 0))
		hprInterval2 = self.pandaActor.hprInterval(3,
												   Point3(0, 0, 0),
												   startHpr=Point3(180, 0, 0))

		# Create and play the sequence that coordinates the intervals.
		self.pandaPace = Sequence(posInterval1, hprInterval1,
								  posInterval2, hprInterval2,
								  name="pandaPace")
		self.pandaPace.loop()

		points = [[0,0,0],[10,0,0],[10,10,0],[10,10,10],[0,10,10],[0,0,10],[0,0,0]]
		self.drawLine(points,width=4)

	def drawLine(self,points,color=None,width=None):
		lines = LineSegs()
		if color:
			lines.setColor(color)
		if width:
			lines.setThickness(width)

		lines.moveTo(*points.pop(0))
		for point in points:
			lines.drawTo(*point)

		node = lines.create()
		np = NodePath(node)
		np.reparentTo(render)

app = MyApp()
app.run()