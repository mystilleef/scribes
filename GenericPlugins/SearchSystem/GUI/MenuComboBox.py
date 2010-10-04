from gettext import gettext as _
data = ((_("Normal"), "normal"), (_("Forward"), "forward"),
	(_("Backward"), "backward"))

class ComboBox(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__quit_cb)
		self.__sigid2 = self.__combo.connect("changed", self.__changed_cb)
		self.__sigid3 = manager.connect("search-type-flag", self.__update_cb)
		self.__populate_model(data)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.menu_gui.get_widget("MenuComboBox")
		self.__model = self.__create_model()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__combo)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
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
		self.__combo.handler_block(self.__sigid2)
		self.__combo.set_property("sensitive", False)
		self.__combo.set_model(None)
		self.__model.clear()
		for search_mode, alias in data: 
			self.__editor.response()
			self.__model.append([search_mode, alias])
		self.__combo.set_model(self.__model)
		self.__combo.set_active(0)
		self.__combo.set_property("sensitive", True)
		self.__combo.handler_unblock(self.__sigid2)
		return False

	def __emit_new_mode(self):
		iterator = self.__combo.get_active_iter()
		search_type = self.__model.get_value(iterator, 1)
		from ..SearchTypeMetadata import set_value
		set_value(search_type)
		self.__manager.emit("reset")
		return False

	def __update_combo(self, search_type):
		self.__combo.handler_block(self.__sigid2)
		dictionary = {"normal": 0, "forward": 1, "backward": 2}
		self.__combo.set_active(dictionary[search_type])
		self.__combo.handler_unblock(self.__sigid2)
		return 

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		self.__emit_new_mode()
		return False

	def __update_cb(self, manager, search_type):
		self.__update_combo(search_type)
		return False
