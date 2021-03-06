class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid4 = manager.connect("match-index", self.__index_cb)
		self.__sigid5 = manager.connect("reset", self.__reset_cb)
		self.__sigid6 = manager.connect("found-matches", self.__found_cb)
		self.__sigid7 = manager.connect("no-search-string", self.__no_search_cb)
		self.__sigid8 = manager.connect("search-mode-flag", self.__search_mode_flag_cb)
		self.__manager.set_data("activate_button", self.__button)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("FindButton")
		self.__string = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
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
		sensitive = False if index == (1, 1) else False
		self.__button.props.sensitive = sensitive
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("search")
		self.__manager.emit("focus-entry")
		return False

	def __search_string_cb(self, manager, string):
		self.__string = string
		sensitive = True if string else False
		self.__button.props.sensitive = sensitive
		return False

	def __search_mode_flag_cb(self, *args):
		sensitive = True if self.__string else False
		self.__button.props.sensitive = sensitive
		return False

	def __index_cb(self, manager, index):
		self.__check_sensitive(index)
		return False

	def __reset_cb(self, *args):
		sensitive = True if self.__string else False
		self.__button.props.sensitive = sensitive
		self.__manager.set_data("activate_button", self.__button)
		return False

	def __found_cb(self, manager, matches):
		if not matches: self.__button.props.sensitive = False
		return False

	def __no_search_cb(self, *args):
		self.__button.props.sensitive = False
		return False
