class Disabler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("filtered-files", self.__files_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __sensitive(self, files):
		value = True if files else False
		self.__view.set_property("sensitive", value)
		return False

	def __files_cb(self, manager, files):
		from gobject import idle_add
		idle_add(self.__sensitive, files)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
