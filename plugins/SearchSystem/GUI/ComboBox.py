from gettext import gettext as _
data = ((_("Default"), "default"), (_("Regular Expression"), "regex"),
	(_("Find As You Type"), "findasyoutype"))

class ComboBox(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__quit_cb)
		self.__sigid2 = self.__combo.connect("changed", self.__changed_cb)
		self.__populate_model(data)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_widget("ComboBox")
		self.__model = self.__create_model()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__combo)
		self.__combo.destroy()
		del self
		self = None
		return

	def __set_properties(self):
		from gtk import CellRendererText
		cell = CellRendererText()
		self.__combo.pack_end(cell, True)
		self.__combo.add_attribute(cell, "text", 0)
		self.__combo.set_model(self.__model)
		return

	def __create_model(self):
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING, TYPE_STRING)
		return model

	def __populate_model(self, data):
		self.__combo.set_property("sensitive", False)
		self.__combo.set_model(None)
		self.__model.clear()
		for search_mode, alias in data:
			self.__model.append([search_mode, alias])
		self.__combo.set_model(self.__model)
		self.__combo.set_active(0)
		self.__combo.set_property("sensitive", True)
		return False

	def __emit_new_mode(self):
		iterator = self.__combo.get_active_iter()
		search_mode = self.__model.get_value(iterator, 1)
		self.__manager.emit("search-mode", search_mode)
		self.__manager.emit("focus-entry")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__emit_new_mode()
		return False