class Updater(object):
	"""
	This class updates a the bookmark database with bookmarked lines
	associated with a document.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect_after("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marked-lines", self.__lines_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __update_database(self, lines):
		if self.__editor.uri in (None, ""): return False
		from Metadata import set_value
		set_value(self.__editor.uri, lines)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __lines_cb(self, manager, lines):
		self.__update_database(lines)
		return False
