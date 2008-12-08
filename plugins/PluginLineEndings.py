name = "Line Endings Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "LineEndingsPlugin"
short_description = "Line ending operations."
long_description = """This plugin performs operations that changes line
endings to unix, mac or windows."""

class LineEndingsPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from LineEndings.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
