class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("row-activated", self.__activated_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_object("TreeView")
		self.__selection = self.__view.get_selection()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __send(self):
		try:
			model, paths = self.__selection.get_selected_rows()
			if not paths: raise ValueError
			get_path = lambda path: model[path][-1]
			filepaths = [get_path(path) for path in paths]
			self.__manager.emit("selected-paths", filepaths)
			self.__manager.emit("hide")
		except ValueError:
			print "no selection to open"
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activated_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__send)
		return True
