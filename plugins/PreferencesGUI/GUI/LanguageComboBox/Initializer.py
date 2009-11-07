class Initializer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__combo = manager.gui.get_object("LanguageComboBox")
		self.__model = self.__create_model()
		return

	def __destroy(self):
		self.__editor.disconnect_signals(((self.__sigid1, self.__manager),))
		del self
		self = None
		return False

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

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
