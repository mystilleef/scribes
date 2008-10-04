name = "Syntax error checker plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.2
autoload = True
class_name = "SyntaxErrorCheckerPlugin"
short_description = "Check Python source code for syntax errors."
long_description = """Check Python source code for syntax errors.
Press F2 to check document."""

class SyntaxErrorCheckerPlugin(object):
	"""
	This class loads and unloads the syntax error checker plugin
	for Python source code.
	"""

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from PythonSyntaxErrorChecker.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
