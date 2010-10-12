class Button(object):

	def __init__(self, editor, manager):
		editor.refresh()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("remove-button-sensitivity", self.__remove_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_widget("RemoveButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		self.__button.destroy()
		del self
		self = None
		return False

	def __remove_cb(self, manager, can_remove):
		self.__button.set_property("sensitive", can_remove)
		return True

	def __clicked_cb(self, *args):
		self.__manager.emit("remove-row")
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return True
