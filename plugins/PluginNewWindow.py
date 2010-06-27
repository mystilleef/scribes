name = "New Window Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "NewWindowPlugin"
short_description = "Open a new editor window."
long_description = """Press ctrl+n to open a new editor window."""

class NewWindowPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from NewWindow.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
