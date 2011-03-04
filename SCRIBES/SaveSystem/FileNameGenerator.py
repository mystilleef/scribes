from gettext import gettext as _

from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "newname", self.__newname_cb)
		from gobject import PRIORITY_LOW, idle_add
		idle_add(self.__optimize, priority=PRIORITY_LOW)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__name = ""
		self.__uri = ""
		self.__stamp = editor.uniquestamp
		return

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
			from gobject import idle_add
			idle_add(self.__manager.emit, "create-new-file", (self.__uri, data))
		except ValueError:
			data = self.__uri, data[1], data[2]
			from gobject import idle_add
			idle_add(self.__manager.emit, "save-data", data)
		return False

	def __filename_on_idle(self, data):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer2 = idle_add(self.__filename, data, priority=PRIORITY_LOW)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 3)]
		return False

	def __optimize(self):
		self.__editor.optimize((self.__filename,))
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __newname_cb(self, manager, data):
		self.__remove_all_timers()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(1000, self.__filename_on_idle, data, priority=PRIORITY_LOW)
		return False
