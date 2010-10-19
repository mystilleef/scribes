name = "Trigger Area Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "TriggerAreaPlugin"
short_description = "Implement trigger area as a plugin."
long_description = """A custom widget that reveals the toolbar and 
menu bar when the mouse is over it."""

class TriggerAreaPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from TriggerArea.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
