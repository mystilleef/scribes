name = "Recent Open Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "RecentOpenPlugin"
short_description = "Quickly open recent files"
long_description = """Open recent files as quickly as possible via a search interface. More effective than using the recent menu."""

class RecentOpenPlugin(object):

	def __init__(self, editor):
		editor.refresh()
		self.__editor = editor
		self.__trigger = None
		editor.refresh()
		
	def load(self):
		self.__editor.refresh()
		from RecentOpen.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.refresh()
		return

	def unload(self):
		self.__editor.refresh()
		self.__trigger.destroy()
		self.__editor.refresh()
		return
