class Opener(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("open-files", self.__open_files_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 

	def __open_files(self, files, encoding):
		self.__editor.open_files(files, encoding)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return 
	
	def __open_files_cb(self, manager, files, encoding):
		from gobject import idle_add
		idle_add(self.__open_files, files, encoding, priority=9999)
		return
