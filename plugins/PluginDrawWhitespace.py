name = "Draw White Spaces"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "WhitespacePlugin"
short_description = "Show the about dialog."
long_description = """This plug-in shows the about dialog."""

class WhitespacePlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from DrawWhitespace.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
