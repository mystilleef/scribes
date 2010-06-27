name = "Python Symbol Browser"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python"]
version = 0.1
autoload = True
class_name = "SymbolBrowserPlugin"
short_description = "Show symbols in python source code."
long_description = """This plugin allows users to view all symbols in
python source code and navigate to them easily. Press F5 to show the
symbol browser."""

class SymbolBrowserPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from PythonSymbolBrowser.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
