class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid4 = manager.connect("match-index", self.__index_cb)
		self.__sigid5 = manager.connect("reset", self.__reset_cb)
		self.__sigid6 = manager.connect("found-matches", self.__found_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("FindButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
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
		return False

	def __search_string_cb(self, manager, string):
		sensitive = True if string else False
		self.__button.props.sensitive = sensitive
		return False

	def __index_cb(self, manager, index):
		self.__check_sensitive(index)
		return False

	def __reset_cb(self, *args):
		self.__button.props.sensitive = True
		return False

	def __found_cb(self, manager, matches):
		if not matches: self.__button.props.sensitive = False
		return False
