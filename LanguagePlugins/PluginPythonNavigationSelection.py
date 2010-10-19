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
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from PythonNavigationSelection.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
