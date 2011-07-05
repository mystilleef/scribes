from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate-uris", self.__generate_uris_cb)
		self.connect(manager, "generate-data-for-treeview", self.__uris_cb)
		self.connect(manager, "finished-enumerating-children", self.__enumerated_children_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__folder_uri = ""
		self.__folder_monitor = None
		self.__uris = []
		self.__unique_id = ""
		return

	def __monitor(self, folder_uri):
		if self.__folder_uri == folder_uri: return False
		self.__disconnect()
		self.__connect(folder_uri)
		return False

	def __connect(self, folder_uri):
		self.__folder_uri = folder_uri
		from gio import File, FILE_MONITOR_WATCH_MOUNTS
		self.__folder_monitor = File(folder_uri).monitor_directory(FILE_MONITOR_WATCH_MOUNTS)
		self.__sigid1 = self.__folder_monitor.connect("changed", self.__changed_cb)
		return False

	def __disconnect(self):
		if not self.__folder_uri: return False
		self.__folder_monitor.disconnect(self.__sigid1)
		self.__folder_monitor.cancel()
		self.__folder_monitor = None
		return False

	def __check(self):
		from uuid import uuid1
		self.__unique_id = str(uuid1())
		from gobject import idle_add
		idle_add(self.__manager.emit, "enumerate-children", (self.__folder_uri, self.__unique_id))
		return False

	def __compare(self, user_data):
		fileinfos, folder_uri, unique_id = user_data
		if unique_id != self.__unique_id: return False
		if folder_uri != self.__folder_uri: return False
		from gio import File
		uris = sorted((File(folder_uri).resolve_relative_path(fileinfo.get_name()).get_uri()
			for fileinfo in fileinfos))
		if uris == self.__uris: return False
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-uris", folder_uri)
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __changed_cb(self, folder_monitor, gfile, other_gfile, event_type):
		from gio import FILE_MONITOR_EVENT_CREATED, FILE_MONITOR_EVENT_DELETED
		if event_type not in (FILE_MONITOR_EVENT_CREATED, FILE_MONITOR_EVENT_DELETED): return False
		self.__remove_timer(1)
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer1 = timeout_add(2000, self.__check, priority=PRIORITY_LOW)
		return False

	def __generate_uris_cb(self, manager, folder_uri):
		from gobject import idle_add
		idle_add(self.__monitor, folder_uri)
		return False

	def __enumerated_children_cb(self, manager, user_data):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compare, user_data, priority=PRIORITY_LOW)
		return False

	def __uris_cb(self, manager, user_data):
		folder_uri, fileinfos, treeview_reference = user_data
		from gio import File
		self.__uris = sorted((File(folder_uri).resolve_relative_path(fileinfo.get_name()).get_uri()
			for fileinfo in fileinfos))
		return False

	def __destroy_cb(self, *args):
		self.__disconnect()
		self.disconnect()
		del self
		return False
