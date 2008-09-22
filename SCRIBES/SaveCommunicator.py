save_dbus_service = "org.sourceforge.ScribesSaveProcessor"

class Communicator(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("send-data-to-processor", self.__send_cb)
		editor.session_bus.add_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=save_dbus_service)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__processor = editor.save_processor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__processor.update(self.__editor.id_, dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		self.__editor.session_bus.remove_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__save_error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=save_dbus_service)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __send(self, uri, encoding):
		self.__processor.process(self.__editor.id_, self.__editor.text,
				uri, encoding,
				dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		return False

################################################################################
#
#							Signal Listeners
#
################################################################################

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __send_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__send, uri, encoding, priority=9999)
		return False

################################################################################
#
#							DBus Signal Listeners
#
################################################################################

	def __saved_file_cb(self, editor_id, uri, encoding):
		if (self.__editor.id_ != editor_id): return False
		from gobject import idle_add
		idle_add(self.__editor.emit, "dbus-saved-file", uri, encoding, priority=9999)
		return False

	def __save_error_cb(self, editor_id, uri, encoding, error_message, error_id):
		if (self.__editor.id_ != editor_id): return False
		self.__editor.emit("dbus-save-error", uri, encoding, error_message)
		return False

	def __is_ready_cb(self, *args):
		self.__processor = self.__editor.save_processor
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, error):
#		self.__editor.emit("dbus-save-error")
		print error
		return False
