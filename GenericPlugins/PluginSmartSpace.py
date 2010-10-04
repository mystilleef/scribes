name = "Smart Space Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "SmartSpacePlugin"
short_description = "Smart space plugin."
long_description = """Smart space plugin."""

class SmartSpacePlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__manager = None
		editor.response()

	def load(self):
		self.__editor.response()
		from SmartSpace.Manager import Manager
		self.__manager = Manager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.destroy()
		self.__editor.response()
		return
