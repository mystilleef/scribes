from SCRIBES.SignalConnectionManager import SignalManager

DBUS_SERVICE = "org.sourceforge.ScribesWordCompletionSuggestionGenerator"

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=DBUS_SERVICE)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__start, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		from os.path import join
		from sys import executable
		self.__editor = editor
		generator_script = "ScribesWordCompletionSuggestionGenerator.py"
		self.__cwd = self.__editor.get_current_folder(globals())
		self.__executable = join(self.__cwd, "SuggestionProcess", generator_script)
		self.__python_executable = executable
		return

	def __start(self):
		if self.__process_exists(): return False
		self.__start_process()
		return False

	def __process_exists(self):
		services = self.__editor.dbus_iface.ListNames()
		if DBUS_SERVICE in services: return True
		return False

	def __start_process(self):
		from gobject import spawn_async, GError
		try:
			args = [self.__python_executable, self.__executable, self.__editor.python_path]
			spawn_async(args, working_directory=self.__cwd)
		except GError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=DBUS_SERVICE)
		del self
		return False

	def __name_change_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__start, priority=PRIORITY_LOW)
		return False
