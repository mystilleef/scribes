class Extractor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("toggled-path", self.__toggled_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = manager.gui.get_widget("TreeView")
		self.__model = self.__view.get_model()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __extract(self):
		encodings = []
		for path in xrange(len(self.__model)):
			self.__editor.response()
			if not self.__model[path][0]: continue
			encodings.append(self.__model[path][1])
		self.__manager.emit("selected-encodings", encodings)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __toggled_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__extract)
		return False
