
class ComboBoxEntry(object):
	"""
	This class creates a comboboxentry for the remote dialog.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__editor.recent_manager.connect("changed", self.__entry_changed_cb)
		self.__sigid2 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid3 = self.__entry.connect("activate", self.__activate_cb)
		self.__sigid4 = manager.connect("load-remote-file", self.__load_file_cb)
		self.__sigid5 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid6 = manager.connect("remote-encoding", self.__encoding_cb)
		from gobject import idle_add
		idle_add(self.__populate_model, priority=9999)
		idle_add(self.__emit_error)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__model = self.__create_model()
		self.__manager = manager
		self.__encoding = "utf8"
		self.__combo = manager.remote_gui.get_widget("ComboBoxEntry")
		self.__entry = manager.remote_gui.get_widget("Entry")
		return

	def __set_properties(self):
		self.__combo.props.model = self.__model
		self.__combo.props.text_column = 0
		return

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __populate_model(self):
		self.__combo.set_property("sensitive", False)
		self.__model.clear()
		recent_infos = self.__editor.recent_manager.get_items()
		for recent_info in recent_infos:
			uri = recent_info.get_uri()
			if uri.startswith("file://"): continue
			self.__model.append([uri])
		self.__combo.set_property("sensitive", True)
		self.__entry.grab_focus()
		return False

	def __load_uri(self):
		self.__manager.emit("hide-remote-dialog-window")
		uri = self.__entry.get_text().strip()
		if not uri: return False
		self.__manager.emit("open-files", [uri], self.__encoding)
		return False

	def __emit_error(self):
		value = True if self.__entry.get_text() else False
		self.__manager.emit("remote-button-sensitivity", value)
		return False

	def __entry_changed_cb(self, recent_manager):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		return True

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit_error)
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_uri)
		return False

	def __load_file_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__load_uri)
		return False

	def __encoding_cb(self, manager, encoding):
		self.__encoding = encoding
		return False

	def __destroy_cb(self, entry):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.recent_manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__entry)
		self.__editor.disconnect_signal(self.__sigid3, self.__entry)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__combo.destroy()
		del self
		self = None
		return
