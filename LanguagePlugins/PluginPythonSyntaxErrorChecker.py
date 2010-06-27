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

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from PythonSyntaxErrorChecker.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
