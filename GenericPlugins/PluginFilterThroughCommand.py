name = "FilterThroughCommand Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "FilterThroughCommandPlugin"
short_description = "Use external programs to process current document"
long_description = "Use external programs to transform the content of the current document. Press <alt>x to show the command interface. You can choose replace the current document with the transformation or have the transformation show in a new window."

class FilterThroughCommandPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from FilterThroughCommand.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
