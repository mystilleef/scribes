from SCRIBES.SignalConnectionManager import SignalManager

dbus_service = "org.sourceforge.ScribesWordCompletionSuggestionGenerator"
dbus_path = "/org/sourceforge/ScribesWordCompletionSuggestionGenerator"

class Communicator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate", self.__generate_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=dbus_service)
		self.__update_generator()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__generator = None
		return

	def __generate(self, string):
		try:
			self.__generator.generate(
				string,
				dbus_interface=dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb
			)
		except AttributeError:
			self.__update_generator()
		except Exception:
			print "ERROR: Cannot send message to word completion suggestion generator"
		return False

	def __update_generator(self):
		self.__generator = None
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (dbus_service in services): return
		self.__generator = session_bus.get_object(dbus_service, dbus_path)
		return

	def __generate_cb(self, manager, string):
		self.__generate(string)
		return False

	def __reply_handler_cb(self, matches):
		emit = self.__manager.emit
		emit("match-found", matches) if matches else emit("no-match-found")
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with word completion indexer"
		return False

	def __name_change_cb(self, *args):
		self.__update_generator()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=dbus_service)
		del self
		return False
