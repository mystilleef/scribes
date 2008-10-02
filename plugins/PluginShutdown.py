name = "Shutdown Scribes"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "ShutdownPlugin"
short_description = "Plug-in to shutdown Scribes."
long_description = """Plug-in to shutdown Scribes."""

class ShutdownPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Shutdown.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
