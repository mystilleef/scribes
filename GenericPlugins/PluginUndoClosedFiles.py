name = "Undo Closed Files Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "UndoClosedFilesPlugin"
short_description = "Reopen recently closed files quickly."
long_description = """Reopen recently closed files very quickly. ctrl+shit+w opens last closed file. ctrl+shift+q opens last 5 closed files."""

class UndoClosedFilesPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from UndoClosedFiles.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
