name = "QuickOpen Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>", "Jeremy Wilkins"]
version = 0.2
autoload = True
class_name = "QuickOpenPlugin"
short_description = "Quickly Open Files."
long_description = """Quickly Open Files."""

class QuickOpenPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from QuickOpen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
