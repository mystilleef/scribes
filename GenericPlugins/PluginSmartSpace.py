name = "Smart Space Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "SmartSpacePlugin"
short_description = "Smart space plugin."
long_description = """Smart space plugin."""

class SmartSpacePlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__manager = None

	def load(self):
		from SmartSpace.Manager import Manager
		self.__manager = Manager(self.__editor)
		return

	def unload(self):
		self.__manager.destroy()
		return
