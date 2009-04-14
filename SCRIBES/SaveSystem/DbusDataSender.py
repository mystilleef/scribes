save_dbus_service = "org.sourceforge.ScribesSaveProcessor"

class Sender(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("session-id", self.__session_cb)
		self.__sigid3 = manager.connect("save-data", self.__data_cb)
		self.__sigid4 = manager.connect("save-processor-object", self.__processor_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__session_id = ()
		self.__processor = None
		return

	def __destroy(self):
		self.__processor.update(self.__editor.id_, dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __send(self, data):
		session_id, uri, encoding = data
		if self.__session_id != session_id: return False
		self.__processor.process(session_id, self.__editor.text, uri, encoding,
				dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __session_cb(self, manager, session_id):
		self.__session_id = session_id
		return False

	def __data_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__send, data, priority=9999)
		return False

	def __processor_cb(self, manager, processor):
		self.__processor = processor
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, error):
		print error
		return False
