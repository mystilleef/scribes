class Button(object):

	def __init__(self, editor, manager):
		editor.response()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("valid-selection", self.__valid_selection_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		editor.response()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.dialog_gui.get_widget("AddButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		self.__button.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __valid_selection_cb(self, manager, value):
		self.__button.set_property("sensitive", value)
		return

	def __clicked_cb(self, *args):
		self.__manager.emit("activate-chooser")
		return
