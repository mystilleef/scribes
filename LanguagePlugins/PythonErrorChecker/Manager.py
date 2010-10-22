from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Feedback import Feedback
		Feedback(self, editor)
		from LineJumper import Jumper
		Jumper(self, editor)
		from Rechecker import Rechecker
		Rechecker(self, editor)
		from PyFlakesChecker import Checker
		Checker(self, editor)
		from SyntaxChecker import Checker
		Checker(self, editor)
		from CheckTimer import Timer
		Timer(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
