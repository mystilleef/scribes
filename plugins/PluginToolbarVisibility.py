name = "Show/Hide Toolbar Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "ToolbarVisibilityPlugin"
short_description = "Show or the toolbar."
long_description = """This plug-in shows or hides the toolbar."""

class ToolbarVisibilityPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from ToolbarVisibility.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
