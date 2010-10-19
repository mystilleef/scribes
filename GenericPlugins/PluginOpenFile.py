name = "Open File Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "OpenFilePlugin"
short_description = "The plugin opens, or creates, files via a GUI."
long_description = """This plug-in opens, or creates files via a GUI."""

class OpenFilePlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from OpenFile.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
