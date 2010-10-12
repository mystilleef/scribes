class Dispatcher(object):

	def __init__(self, editor, manager):
		editor.refresh()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("scan-schemes", self.__scan_themes_cb)
		self.__scheme_manager.force_rescan()
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__scheme_manager = editor.style_scheme_manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __dispatch_schemes(self):
		self.__scheme_manager.force_rescan()
		get_scheme = self.__scheme_manager.get_scheme
		schemes = [get_scheme(id_) for id_ in self.__scheme_manager.get_scheme_ids()]
		self.__manager.emit("schemes", schemes)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __scan_themes_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__dispatch_schemes)
		return False
