name = "Side Pane File Browser Plugin"
authors = ["Hossam Saraya <hossam.saraya@gmail.com>", "Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.3
autoload = True
class_name = "SidePaneFileBrowserPlugin"
short_description = "A side pane file browser"
long_description = "Navigate your file system and open files. Press F4 to show the file browser"

class SidePaneFileBrowserPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from SidePaneFileBrowser.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
