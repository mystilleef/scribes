name = "Line Operations"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "LinesPlugin"
short_description = "Plug-in to perform line operations."
long_description = """Plug-in to perform line operations."""

class LinesPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from Lines.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
