from SCRIBES.SignalConnectionManager import SignalManager

class Collector(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__recent_manager, "changed", self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__filter, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__infos = []
		from gtk import recent_manager_get_default
		self.__recent_manager = recent_manager_get_default()
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __is_scribes_resource(self, info):
		return info.has_application("scribes")

	def __resource_exists(self, info):
		return info.exists()

	def __compare(self, x, y):
		return cmp(x.get_modified(), y.get_modified())

	def __filter(self):
		infos = iter(self.__recent_manager.get_items())
		scribes_infos = (info for info in infos if self.__is_scribes_resource(info))
		exist_infos = (info for info in scribes_infos if self.__resource_exists(info))
		sorted_infos = iter(sorted(exist_infos, cmp=self.__compare, reverse=True))
		self.__manager.emit("recent-infos", sorted_infos)
		return False

	def __filter_timeout(self):
		from gobject import idle_add
		self.__timer = idle_add(self.__filter, priority=999999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(1000, self.__filter_timeout, priority=999999)
		return False
