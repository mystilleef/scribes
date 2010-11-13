name = "Line Jumper Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "LineJumperPlugin"
short_description = "Move cursor to a specific line"
long_description = """Press Ctrl+i to move the cursor to specific line."""

class LineJumperPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from LineJumper.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
