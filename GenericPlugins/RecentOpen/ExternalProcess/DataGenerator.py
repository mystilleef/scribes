from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager
from Utils import pretty_date

class Generator(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(self.__manager, "recent-infos", self.__infos_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		from SCRIBES.Globals import home_folder
		self.__home_folder = home_folder
		return

	def __get_language(self, mimetype):
		self.__manager.response()
		from gio import content_type_get_description as get_desc
		return get_desc(mimetype).split()[0].lower()

	def __get_search_path_from(self, uri):
		self.__manager.response()
		from gio import File
		path = File(uri).get_parse_name()
		path = path.replace(self.__home_folder, "").strip("/\\")
		self.__manager.response()
		return path

	def __get_display_path_from(self, uri):
		self.__manager.response()
		from gio import File
		path = File(uri).get_parent().get_parse_name()
		path = path.replace(self.__home_folder, "").strip("/\\")
		from os.path import split
		self.__manager.response()
		if not path: return split(self.__home_folder)[-1].strip("/\\")
		return path

	def __format(self, info):
		self.__manager.response()
		uri = info.get_uri()
		self.__manager.response()
		file_path = self.__get_search_path_from(uri)
		self.__manager.response()
		display_path = self.__get_display_path_from(uri)
		self.__manager.response()
		display_name = info.get_display_name()
		self.__manager.response()
		modified = pretty_date(info.get_modified())
		self.__manager.response()
		location = "" if info.is_local() else _("remote")
		self.__manager.response()
		filetype = self.__get_language(info.get_mime_type())
		self.__manager.response()
		icon = info.get_icon(32)
		self.__manager.response()
		return file_path, icon, display_name, display_path, modified, location, filetype, uri

	def __process(self, infos):
		self.__manager.response()
		data = [self.__format(info) for info in infos]
		self.__manager.emit("recent-infos-data", data)
		self.__manager.emit("recent-uris", [_data[-1] for _data in data])
		return False

	def __infos_cb(self, manager, infos):
		from gobject import idle_add
		idle_add(self.__process, infos)
		return False
