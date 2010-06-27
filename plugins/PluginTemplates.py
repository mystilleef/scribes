name = "Dynamic Templates Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "TemplatesPlugin"
short_description = "Dynamic Templates"
long_description = """This plug-in performs templates operations"""

class TemplatesPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__manager = None
		editor.response()

	def load(self):
		self.__editor.response()
		from Templates.Manager import Manager
		self.__manager = Manager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.destroy()
		self.__editor.response()
		return
