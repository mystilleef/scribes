class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search", self.__search_cb)
		self.__sigid3 = manager.connect("search-type-flag", self.__update_cb)
		self.__sigid4 = manager.connect("selection-bounds", self.__selection_bounds_cb)
		self.__sigid5 = manager.connect("hide-bar", self.__hide_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__type = "normal"
		self.__selection_bounds = None
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return 

	def __send_boundary(self):
		if self.__selection_bounds:
			bounds = self.__selection_bounds
		elif self.__type == "normal":
			bounds = self.__editor.textbuffer.get_bounds()
		elif self.__type == "forward":
			bounds = self.__editor.textbuffer.get_bounds()
			bounds = self.__editor.cursor, bounds[1]
		else:
			bounds = self.__editor.textbuffer.get_bounds()
			bounds = bounds[0], self.__editor.cursor
		self.__manager.emit("search-boundary", bounds)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return 

	def __search_cb(self, *args):
		self.__send_boundary()
		return False

	def __update_cb(self, manager, search_type):
		self.__type = search_type
		return False

	def __selection_bounds_cb(self, manager, bounds):
		self.__selection_bounds = bounds
		return False

	def __hide_cb(self, *args):
		self.__selection_bounds = None
		return False
