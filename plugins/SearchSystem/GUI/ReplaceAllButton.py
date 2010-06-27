class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("reset", self.__reset_cb)
		self.__sigid3 = manager.connect("hide-bar", self.__reset_cb)
		self.__sigid4 = manager.connect("search-string", self.__reset_cb)
		self.__sigid5 = manager.connect("found-matches", self.__found_matches_cb)
		self.__sigid7 = manager.connect("no-search-string", self.__reset_cb)
		self.__sigid6 = self.__button.connect("clicked", self.__clicked_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("ReplaceAllButton")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__button)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __reset_cb(self, *args):
		self.__button.props.sensitive = False
		return False

	def __found_matches_cb(self, manager, matches):
		sensitive = True if len(matches) > 1 else False
		self.__button.props.sensitive = sensitive
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("replace-all")
		self.__manager.emit("focus-replace-entry")
		return False
