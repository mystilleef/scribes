from Utils import response

class Manager(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		self.__recent_manager.connect("changed", self.__changed_cb)
		self.__update()
#		from gobject import idle_add
#		idle_add(self.__update)

	def recent_infos(self):
		return self.__infos

	def recent_manager(self):
		return self.__recent_manager

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__infos = []
		from gtk import recent_manager_get_default
		self.__recent_manager = recent_manager_get_default()
		return

	def __is_scribes_resource(self, info):
		response()
		return info.has_application("scribes")

	def __resource_exists(self, info):
		response()
		if info.is_local() is False: return True
		return info.exists()

	def __compare(self, x, y):
		response()
		return cmp(x.get_modified(), y.get_modified())

	def __update(self):
		self.__infos = self.__get_infos()
		return False

	def __get_infos(self):
		infos = iter(self.__recent_manager.get_items())
		scribes_infos = (info for info in infos if self.__is_scribes_resource(info))
		exist_infos = (info for info in scribes_infos if self.__resource_exists(info))
		return sorted(exist_infos, cmp=self.__compare, reverse=True)

	def __update_timeout(self):
		from glib import PRIORITY_LOW
		from gobject import idle_add
		self.__timer = idle_add(self.__update, priority=PRIORITY_LOW)
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			from glib import PRIORITY_LOW
			self.__timer = timeout_add(1000, self.__update_timeout, priority=PRIORITY_LOW)
		return False
