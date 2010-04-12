from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Displayer import Displayer
		Displayer(self, editor)
		from Widget import Widget
		Widget(self, editor)

	def show(self):
		self.emit("show")
		return False

	def hide(self):
		self.emit("hide")
		return False
