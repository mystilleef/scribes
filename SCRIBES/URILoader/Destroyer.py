class Destroyer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = editor.connect_after("loaded-file", self.__loaded_file_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.textview.grab_focus()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		del self.__manager
		del self
		self = None
		return False

	def __emit(self):
		self.__manager.emit("destroy")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __loaded_file_cb(self, *args):
		from gobject import timeout_add
		from glib import PRIORITY_LOW
		timeout_add(1000, self.__emit, priority=PRIORITY_LOW)
		return False
