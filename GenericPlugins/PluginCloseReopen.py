name = "CloseReopen Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "CloseReopenPlugin"
short_description = "Close current window, reopen new one."
long_description = """Close current window, reopen new one."""

class CloseReopenPlugin(object):

	def __init__(self, editor):
		self.__editor = editor

	def load(self):
		from CloseReopen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
