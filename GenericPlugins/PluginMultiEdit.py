name = "Multi Edit Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "MultiEditPlugin"
short_description = "Edit several places in the editing area simultaneously"
long_description = """Press <ctrl><shift>i to enable multi editing
mode. <ctrl>i adds or removes edit points in the editing area. Type
to edit the edit points simultaneously."""

class MultiEditPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from MultiEdit.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
