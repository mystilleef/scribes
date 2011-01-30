from Signals import Signal 

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Bindings.Manager import Manager
		Manager(editor)
		from Quiter import Quiter
		Quiter(self, editor)
		from TriggerManager import Manager
		Manager(self, editor)
		from TriggerActivator import Activator
		Activator(self, editor)
		from AcceleratorActivator import Activator
		Activator(self, editor)
		from TriggerRemover import Remover
		Remover(self, editor)
		from Validator import Validator
		Validator(self, editor)
