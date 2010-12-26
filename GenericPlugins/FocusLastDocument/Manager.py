from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from KeyboardHandler import Handler
		Handler(self, editor)
		from Switcher import Switcher
		Switcher(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False

