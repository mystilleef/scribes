class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid3 = manager.connect("match-index", self.__index_cb)
		self.__sigid4 = manager.connect("reset", self.__reset_cb)
		self.__sigid6 = manager.connect("hide-bar", self.__reset_cb)
		self.__sigid5 = manager.connect("back-button", self.__activate_cb)
		self.__sigid7 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid8 = manager.connect("no-search-string", self.__reset_cb)
		self.__button.props.sensitive = False

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("PreviousButton")
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __check_sensitive(self, index):
		sensitive = False if index[0] == 1 else True
		self.__button.props.sensitive = sensitive
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("previous")
		self.__manager.emit("focus-entry")
		return False

	def __index_cb(self, manager, index):
		self.__check_sensitive(index)
		return False

	def __reset_cb(self, *args):
		self.__button.props.sensitive = False
		return False

	def __activate_cb(self, *args):
		self.__button.activate()
		return False

	def __search_string_cb(self, manager, string):
		self.__button.props.sensitive = False
		return False
