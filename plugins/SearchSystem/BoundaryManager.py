class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search", self.__search_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__forward = False
		self.__backward = False
		return  

	def __send_boundary(self):
		bounds = self.__editor.textbuffer.get_bounds()
		self.__manager.emit("search-boundary", bounds)
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return 

	def __search_cb(self, *args):
		self.__send_boundary()
		return False
