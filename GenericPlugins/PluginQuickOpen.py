name = "QuickOpen Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>", "Jeremy Wilkins"]
version = 0.3
autoload = True
class_name = "QuickOpenPlugin"
short_description = "Quickly Open Files."
long_description = """Quickly Open Files."""

class QuickOpenPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from QuickOpen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
