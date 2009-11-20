from gettext import gettext as _

class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("newname", self.__newname_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__name = ""
		self.__uri = ""
		self.__stamp = editor.uniquestamp
		return

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__editor),
			(self.__sigid1, self.__manager),
		)
		self.__editor.disconnect_signals(signals_data)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __filename(self, _data):
		try:
			newname, data = _data
			if not newname: newname = _("Unnamed Document")
			if self.__name == newname: raise ValueError
			self.__name = newname
			newname = newname + " - " + "(" + self.__stamp + ")"
			newfile = self.__editor.desktop_folder + "/" + newname
			from gio import File
			self.__uri = File(newfile).get_uri()
			self.__manager.emit("create-new-file", (self.__uri, data))
		except ValueError:
			data = self.__uri, data[1], data[2]
			self.__manager.emit("save-data", data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __newname_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__filename, data, priority=9999)
		return False
