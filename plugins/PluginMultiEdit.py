name = "Multi Edit Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "MultiEditPlugin"
short_description = "Edit several places in the editing area simultaneously"
long_description = """Press <ctrl><shift>i to enable multi editing
mode. <ctrl>i adds or removes edit points in the editing area. Type
to edit the edit points simultaneously."""

class MultiEditPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from MultiEdit.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
