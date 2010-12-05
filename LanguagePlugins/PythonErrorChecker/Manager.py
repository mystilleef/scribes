from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Feedback import Feedback
		Feedback(self, editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from Checker import Checker
		Checker(self, editor)
		from ProcessCommunicator import Communicator
		Communicator(self, editor)
		from ExternalProcessStarter import Starter
		Starter(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self, signal):
		self.emit(signal)
		return False
