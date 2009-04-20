from SCRIBES.Globals import SCRIBES_SAVE_PROCESS_DBUS_SERVICE

class Monitor(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		editor.session_bus.add_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		self.__manager.emit("save-processor-object", self.__editor.save_processor)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.session_bus.remove_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=SCRIBES_SAVE_PROCESS_DBUS_SERVICE)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __is_ready_cb(self, *args):
		self.__manager.emit("save-processor-object", self.__editor.save_processor)
		return False
