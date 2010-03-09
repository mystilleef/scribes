from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Displayer import Displayer
		Displayer(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return False

	def show(self):
		self.emit("show")
		return False
