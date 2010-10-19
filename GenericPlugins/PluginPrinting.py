name = "Printing Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.4
autoload = True
class_name = "PrintingPlugin"
short_description = "Shows the about dialog."
long_description = """Shows the about dialog."""

class PrintingPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Printing.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
