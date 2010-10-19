from SCRIBES.SignalConnectionManager import SignalManager
from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_SERVICE

class Receiver(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "session-id", self.__session_cb)
		editor.session_bus.add_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		editor.session_bus.add_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__session_id = ()
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		self.__editor.session_bus.remove_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		self.__editor.unregister_object(self)
		del self
		return False

	def __emit(self, data):
		if self.__editor.id_ != data[0][0]: return False
		if tuple(data[0]) != self.__session_id: return False
		signal_name = "save-succeeded" if len(data) == 3 else "save-failed"
		self.__manager.emit(signal_name, data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __saved_file_cb(self, data):
		from gobject import idle_add
		idle_add(self.__emit, data, priority=9999)
		return False

	def __save_error_cb(self, data):
		from gobject import idle_add
		idle_add(self.__emit, data, priority=9999)
		return False
