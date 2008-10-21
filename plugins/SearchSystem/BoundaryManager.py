class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search", self.__search_cb)
		self.__sigid3 = manager.connect("database-update", self.__update_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__type = "normal"
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __send_boundary(self):
		if self.__editor.selection_range > 1:
			bounds = self.__editor.selection_bounds
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

	def __update_flags(self):
		from SearchTypeMetadata import get_value
		self.__type = get_value()
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return 

	def __search_cb(self, *args):
		self.__send_boundary()
		return False

	def __update_cb(self, *args):
		self.__update_flags()
		return False
