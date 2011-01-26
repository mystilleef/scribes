from SCRIBES.SignalConnectionManager import SignalManager

indexer_dbus_service = "org.sourceforge.ScribesWordCompletionIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesWordCompletionIndexer"

class Communicator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "index", self.__index_cb, True)
		self.connect(editor, "saved-file", self.__saved_cb, True)
		self.connect(editor, "loaded-file", self.__saved_cb, True)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		self.__start_index()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__indexer = self.__get_indexer()
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
			'NameOwnerChanged',
			'org.freedesktop.DBus',
			'org.freedesktop.DBus',
			'/org/freedesktop/DBus',
			arg0=indexer_dbus_service)
		del self
		return False

	def __start_index(self):
		if not self.__indexer: return False
		# Avoid unnecessary calls to the indexer when launching multiple editors.
		if self.__editor.window_is_active is False: return False
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__index, priority=PRIORITY_LOW)
		return False

	def __get_indexer(self):
		from SCRIBES.Globals import dbus_iface, session_bus
		services = dbus_iface.ListNames()
		if not (indexer_dbus_service in services): return None
		indexer = session_bus.get_object(indexer_dbus_service, indexer_dbus_path)
		return indexer

	def __index(self):
		try:
			self.__indexer.index(dbus_interface=indexer_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except AttributeError:
#			print "ERROR:No word completion indexer process found"
			self.__indexer = self.__get_indexer()
		except Exception:
			print "ERROR: Cannot send message to word completion indexer"
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __name_change_cb(self, *args):
		self.__indexer = self.__get_indexer()
		self.__start_index()
		return False

	def __reply_handler_cb(self, *args):
		return False

	def __error_handler_cb(self, *args):
		print "ERROR: Failed to communicate with word completion indexer"
		return False

	def __saved_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__index, priority=PRIORITY_LOW)
		return False

	def __index_cb(self, *args):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__index, priority=PRIORITY_LOW)
		return False
