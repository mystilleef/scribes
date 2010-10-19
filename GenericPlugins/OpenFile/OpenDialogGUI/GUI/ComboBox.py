class ComboBox(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__quit_cb)
		self.__sigid2 = editor.connect("combobox-encoding-data", self.__encoding_data_cb)
		self.__sigid3 = self.__combo.connect("changed", self.__changed_cb)
		editor.emit_combobox_encodings()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.open_gui.get_object("EncodingComboBox")
		self.__model = self.__create_model()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__combo)
		del self
		self = None
		return

	def __set_properties(self):
		from gtk import CellRendererText
		cell = CellRendererText()
		self.__combo.pack_end(cell, True)
		self.__combo.add_attribute(cell, "text", 0)
		self.__combo.set_model(self.__model)
		self.__combo.set_row_separator_func(self.__separator_function)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING, TYPE_STRING)
		return model

	def __separator_function(self, model, iterator):
		if model.get_value(iterator, 0) == "Separator" : return True
		return False

	def __populate_model(self, data):
		self.__combo.set_property("sensitive", False)
		self.__combo.set_model(None)
		self.__model.clear()
		self.__model.append([data[0][0], data[0][1]])
		self.__model.append(["Separator", "Separator"])
		for alias, encoding in data[1:]:
			self.__model.append([alias, encoding])
		self.__model.append(["Separator", "Separator"])
		self.__model.append(["Add or Remove Encoding...", "show_encoding_window"])
		self.__combo.set_model(self.__model)
		self.__combo.set_active(0)
		self.__combo.set_property("sensitive", True)
		return False

	def __emit_new_encoding(self):
		iterator = self.__combo.get_active_iter()
		encoding = self.__model.get_value(iterator, 1)
		if encoding == "show_encoding_window":
			self.__combo.set_active(0)
			self.__editor.show_supported_encodings_window(self.__manager.open_gui.get_widget("Window"))
		else:
			self.__manager.emit("open-encoding", encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __encoding_data_cb(self, editor, data):
		self.__populate_model(data)
		return False

	def __changed_cb(self, *args):
		self.__emit_new_encoding()
		return False
