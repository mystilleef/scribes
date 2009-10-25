class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("save-button-activate", self.__activate_cb)
		self.__sigid3 = self.__chooser.connect("file-activated", self.__activate_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.gui.get_object("FileChooser")
		return

	def __emit(self):
		try:
			self.__editor.response()
			uri = self.__chooser.get_uri()
			if self.__editor.uri_is_folder(uri): raise ValueError
			self.__manager.emit("validate")
			self.__editor.response()
		except ValueError:
			self.__manager.emit("change-folder", uri)
		finally:
			self.__editor.response()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__emit)
		return False
