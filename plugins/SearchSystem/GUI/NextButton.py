class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid3 = manager.connect("match-index", self.__index_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__button.props.sensitive = False

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("NextButton")
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __check_sensitive(self, index):
		sensitive = False if index[0] == index[1] else True
		self.__button.props.sensitive = sensitive
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("next")
		self.__manager.emit("focus-entry")
		return False

	def __index_cb(self, manager, index):
		self.__check_sensitive(index)
		return False

	def __reset_cb(self, *args):
		self.__button.props.sensitive = False
		return False
