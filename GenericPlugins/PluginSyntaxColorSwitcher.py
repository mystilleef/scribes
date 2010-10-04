name = "Syntax Color Switcher Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = False
class_name = "SyntaxColorSwitcherPlugin"
short_description = "Switch syntax colors"
long_description = """This plugin enables users to set syntax colors \
for documents for a specific language via the popup menu.
"""

class SyntaxColorSwitcherPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__manager = None
		editor.response()

	def load(self):
		self.__editor.response()
		from SyntaxColorSwitcher.Manager import Manager
		self.__manager = Manager(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__manager.emit("destroy")
		self.__editor.response()
		return
