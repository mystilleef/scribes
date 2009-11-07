name = "Preferences Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "PreferencesGUIPlugin"
short_description = "GUI to customize the behavior of the editor."
long_description = """Implements the GUI to customize the behavior of
the editor"""

class PreferencesGUIPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from PreferencesGUI.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
