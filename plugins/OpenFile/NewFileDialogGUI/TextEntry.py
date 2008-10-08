class Entry(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__entry.connect("changed", self.__changed_cb)
		self.__sigid3 = manager.connect("create", self.__create_cb)
		self.__sigid4 = manager.connect("show-newfile-dialog-window", self.__show_cb)
		self.__entry.props.sensitive = True
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__entry = manager.new_gui.get_widget("TextEntry")
		return False
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__entry)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__entry.destroy()
		del self
		self = None
		return False
	
	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __changed_cb(self, *args):
		name = self.__entry.get_text()
		self.__manager.emit("validate", name)
		return False
	
	def __create_cb(self, *args):
		name = self.__entry.get_text()
		self.__manager.emit("create-file", name)
		return False

	def __show_cb(self, *args):
		self.__entry.set_text("")
		return False
