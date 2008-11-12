name = "Preferences Plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "PreferencesPlugin"
short_description = "Shows the dialog that customizes the editor."
long_description = """Shows the dialog that customizes the editor."""

class PreferencesPlugin(object):

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from Preferences.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
