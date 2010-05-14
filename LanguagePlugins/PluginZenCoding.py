name = "Zen Coding Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
languages = ["html", "xml", "css"]
autoload = True
class_name = "ZenCodingPlugin"
short_description = "Zen Coding Plugin"
long_description = """Zen Coding Plugin"""

class ZenCodingPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from zencoding.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
