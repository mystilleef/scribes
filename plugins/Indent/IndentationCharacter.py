class Character(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("indent", self.__process_cb)
		self.__sigid3 = manager.connect("unindent", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 

	def __send_character(self):
		use_spaces = self.__editor.textview.get_insert_spaces_instead_of_tabs()
		if use_spaces:
			width = self.__editor.textview.get_tab_width()
			self.__manager.emit("character", (" " * width))
		else:
			self.__manager.emit("character", "\t")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, *args):
		self.__send_character()
		return False
