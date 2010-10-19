from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "newname", self.__newname_cb)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__name = ""
		self.__uri = ""
		self.__stamp = editor.uniquestamp
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __filename(self, _data):
		try:
			newname, data = _data
			if not newname: newname = _("Unnamed Document")
			if self.__name == newname: raise ValueError
			self.__name = newname
			newname = newname + " - " + "(" + self.__stamp + ")"
			from os.path import join
			newfile = join(self.__editor.desktop_folder, newname)
			from gio import File
			self.__uri = File(newfile).get_uri()
			self.__manager.emit("create-new-file", (self.__uri, data))
		except ValueError:
			data = self.__uri, data[1], data[2]
			self.__manager.emit("save-data", data)
		return False

	def __optimize(self):
		self.__editor.optimize((self.__filename,))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __newname_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__filename, data, priority=9999)
		return False
