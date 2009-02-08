class Extractor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("updating-database", self.__updating_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__name_entry = manager.editor_gui.get_widget("NameEntry")
		self.__description_entry = manager.editor_gui.get_widget("DescriptionEntry")
		self.__buffer = manager.editor_gui.get_widget("ScrolledWindow").get_child().get_buffer()
		return

	def __send_data(self):
		trigger = self.__name_entry.get_text()
		description = self.__description_entry.get_text()
		template = self.__buffer.get_text(*self.__buffer.get_bounds())
		self.__manager.emit("gui-template-editor-data", (trigger, description, template))
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updating_cb(self, *args):
		self.__send_data()
		return False
