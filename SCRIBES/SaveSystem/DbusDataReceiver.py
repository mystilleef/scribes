save_dbus_service = "org.sourceforge.ScribesSaveProcessor"

class Receiver(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("session-id", self.__session_cb)
		editor.session_bus.add_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__session_id = ()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.session_bus.remove_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __emit(self, data):
		if self.__session_id != data[0]: return False
		signal_name = "save-succeeded" if len(data) == 3 else "save-failed"
		self.__manager.emit(signal_name, data)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __saved_file_cb(self, session_id, uri, encoding):
		data = session_id, uri, encoding
		from gobject import idle_add
		idle_add(self.__emit, data, priority=9999)
		return False

	def __save_error_cb(self, session_id, uri, encoding, error_message, error_id):
		data = session_id, uri, encoding, error_message, error_id
		from gobject import idle_add
		idle_add(self.__emit, data, priority=9999)
		return False
