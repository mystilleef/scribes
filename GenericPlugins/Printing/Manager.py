from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Feedback import Feedback
		Feedback(self, editor)
		from Displayer import Displayer
		Displayer(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
