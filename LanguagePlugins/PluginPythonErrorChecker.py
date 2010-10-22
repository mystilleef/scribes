name = "Python error checker plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.2
autoload = True
class_name = "ErrorCheckerPlugin"
short_description = "Automatically check Python source code for errors."
long_description = """Automatically check Python source code for common syntax, semantic and logic errors."""

class ErrorCheckerPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from PythonErrorChecker.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
