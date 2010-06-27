name = "About Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "AboutPlugin"
short_description = "Shows the about dialog."
long_description = """Shows the about dialog."""

class AboutPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from About.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
