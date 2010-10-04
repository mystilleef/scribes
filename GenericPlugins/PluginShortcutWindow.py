name = "Shortcut Window Plugin"
authors = ["Kuba"]
version = 0.3
autoload = True
class_name = "ShortcutWindowPlugin"
short_description = "Shows all shortcuts"
long_description = """This plugin creates a handy window listing
all shortcuts available in Scribes."""

class ShortcutWindowPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from ShortcutWindow.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
