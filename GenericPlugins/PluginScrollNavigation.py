name = "Scroll Navigation Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "ScrollNavigationPlugin"
short_description = "Keyboard Scroll navigation for Scribes."
long_description = """Keyboard Scroll navigation for Scribes."""

class ScrollNavigationPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from ScrollNavigation.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
