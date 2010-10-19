class Manager(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		self.__recent_manager.connect("changed", self.__changed_cb)
		from gobject import idle_add
		idle_add(self.__update, priority=9999)

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
		return info.has_application("scribes")

	def __resource_exists(self, info):
		return info.exists()

	def __compare(self, x, y):
		return cmp(x.get_modified(), y.get_modified())

	def __update(self):
		self.__infos = self.__get_infos()
		return False

	def __get_infos(self):
		infos = iter(self.__recent_manager.get_items())
		scribes_infos = (info for info in infos if self.__is_scribes_resource(info))
		exist_infos = (info for info in scribes_infos if self.__resource_exists(info))
		return sorted(exist_infos, cmp=self.__compare, reverse=True)

	def __update_editors(self):
		self.__update()
		[editor.emit("recent-infos", self.__infos) for editor in self.__manager.get_editor_instances()]
		return False

	def __update_editors_timeout(self):
		from gobject import idle_add
		self.__timer = idle_add(self.__update_editors, priority=999999)
		return False

	def __changed_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(1000, self.__update_editors_timeout, priority=999999)
		return False
