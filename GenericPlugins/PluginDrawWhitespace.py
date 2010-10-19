name = "Draw White Spaces"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "WhitespacePlugin"
short_description = "Show the about dialog."
long_description = """This plug-in shows the about dialog."""

class WhitespacePlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from DrawWhitespace.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
