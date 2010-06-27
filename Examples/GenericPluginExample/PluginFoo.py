name = "Foo Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "FooPlugin"
short_description = "Unleashes Foo's awesome powers!"
long_description = """A demonstration plugin that shows an information
window and updates the message bar. This plugin shows plugin designers
how to write plugins and structure code in Scribes"""

class FooPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()
		
	def load(self):
		self.__editor.response()
		from Foo.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
