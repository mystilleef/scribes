class Listener(object):

	def __init__(self, manager):
		from gtk import recent_manager_get_default
		rmanager = recent_manager_get_default()
		rmanager.connect("changed", self.__changed_cb, manager)
		self.__update(manager)

	def __compare(self, x, y):
		return cmp(x.get_modified(), y.get_modified())

	def __resource_exists(self, info):
		if info.is_local() is False: return True
		return info.exists()

	def __is_scribes_resource(self, info):
		return info.has_application("scribes")

	def __get_infos(self):
		from gtk import recent_manager_get_default
		infos = iter(recent_manager_get_default().get_items())
		scribes_infos = (info for info in infos if self.__is_scribes_resource(info))
		exist_infos = (info for info in scribes_infos if self.__resource_exists(info))
		return sorted(exist_infos, cmp=self.__compare, reverse=True)

	def __update(self, manager):
		manager.emit("recent-infos", self.__get_infos())
		return False

	def __update_timeout(self, manager):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update, manager, priority=PRIORITY_LOW)
		return False

	def __changed_cb(self, rmanager, manager):
		try:
			from gobject import timeout_add, source_remove, PRIORITY_LOW
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(1000, self.__update_timeout, manager, priority=PRIORITY_LOW)
		return False
