name = "Smart indentation plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "SmartIndentationPlugin"
short_description = "Smart indentation for Python source code."
long_description = """Smart indentation for Python source code."""

class SmartIndentationPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__manager = None
		editor.response()

	def load(self):
		self.__editor.response()
		from PythonSmartIndentation.Manager import Manager
		self.__manager = Manager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.destroy()
		self.__editor.response()
		return
