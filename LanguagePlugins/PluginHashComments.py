
name = "Hash (un)comment plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
languages = ["python", "ruby", "perl", "sh"]
version = 0.2
autoload = True
class_name = "CommentPlugin"
short_description = "(Un)comment lines in source code"
long_description = """This plugin allows users to (un)comment lines in
hash source code by pressing (alt - c)"""

class CommentPlugin(object):
	"""
	Load and initialize comment plugin for several source code.
	"""

	def __init__(self, editor):
		self.__editor = editor
		self.__trigger = None

	def load(self):
		from HashComments.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		self.__trigger.destroy()
		return
