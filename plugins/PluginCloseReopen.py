name = "CloseReopen Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "CloseReopenPlugin"
short_description = "Close current window, reopen new one."
long_description = """Close current window, reopen new one."""

class CloseReopenPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		editor.response()

	def load(self):
		self.__editor.response()
		from CloseReopen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
