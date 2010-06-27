name = "Advanced configuration plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "AdvancedConfigurationPlugin"
short_description = "Shows the advanced configuration window."
long_description = """Shows the advanced configuration window. The
window allows user to configure advanced options provided by the
editor."""

class AdvancedConfigurationPlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from AdvancedConfiguration.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
