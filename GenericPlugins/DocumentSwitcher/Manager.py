from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Switcher import Switcher
		Switcher(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return 

	def activate(self, command):
		self.emit(command)
		return
