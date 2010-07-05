from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from HideTimer import Timer
		Timer(self, editor)
		from Animator import Animator
		Animator(self, editor)
		from DeltaCalculator import Calculator
		Calculator(self, editor)
		from PublicAPIVisibilityUpdater import Updater
		Updater(self, editor)
		from VisibilityUpdater import Updater
		Updater(self, editor)
		from Displayer import Displayer
		Displayer(self, editor)
		from DisplayerManager import Manager
		Manager(self, editor)
		from ViewSizeUpdater import Updater
		Updater(self, editor)
		from BarSizeUpdater import Updater
		Updater(self, editor)
		from EventBoxColorChanger import Changer
		Changer(self, editor)
		from Widget import Widget
		Widget(self, editor)

	def show(self):
		self.emit("show")
		return False

	def hide(self):
		self.emit("hide")
		return False
