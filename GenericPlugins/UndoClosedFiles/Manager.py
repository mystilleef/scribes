from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from UriOpener import Opener
		Opener(self, editor)
		from DataGenerator import Generator
		Generator(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self, signal):
		self.emit(signal)
		return False
