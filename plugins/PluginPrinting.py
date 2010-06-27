name = "Printing Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "PrintingPlugin"
short_description = "Shows the about dialog."
long_description = """Shows the about dialog."""

class PrintingPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from Printing.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
