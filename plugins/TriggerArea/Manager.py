from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from TriggerWidget import TriggerWidget
		self.set_data("TriggerWidget", TriggerWidget())
		from TriggerHandler import Handler
		Handler(self, editor)
		from Positioner import Positioner
		Positioner(self, editor)
		from Displayer import Displayer
		Displayer(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False
