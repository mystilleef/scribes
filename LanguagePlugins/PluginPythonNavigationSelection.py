name = "Navigation and selection plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.2
autoload = True
class_name = "NavigationSelectionPlugin"
short_description = "Navigation and selection for Python source code."
long_description = """Navigation and selection for Python source code."""

class NavigationSelectionPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from PythonNavigationSelection.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
