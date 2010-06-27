name = "User Guide Plug-in"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.2
autoload = True
class_name = "UserGuidePlugin"
short_description = "Show Scribes' user guide."
long_description = """\
This plug-in launching the Scribes's help browser, yelp.
"""

class UserGuidePlugin(object):

	def __init__(self, editor):
		editor.response()
		self.__editor = editor
		self.__trigger = None
		editor.response()

	def load(self):
		self.__editor.response()
		from UserGuide.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		self.__editor.response()
		return

	def unload(self):
		self.__editor.response()
		self.__trigger.destroy()
		self.__editor.response()
		return
